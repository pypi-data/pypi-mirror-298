# This file contains code snippets from fastapi-key-auth
# licensed under the MIT License.
# https://github.com/iwpnd/fastapi-key-auth/tree/main/fastapi_key_auth
#
# MIT License

# Copyright (c) 2021 Benjamin Ramser

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNES FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Modifications:
#
# - Dylan 2024-09-07: make it work with arbitrary headers, and dynamic
#   authentication calls

"""
FastAPI API-key authentication middleware and dependency.
"""

__all__ = [
    "ApiKeyAuthenticationMiddleware",
    "api_key_authentication_info",
    "Authenticator",
    "AuthChecker",
    "AuthInfoDep",
]

from dataclasses import dataclass
import enum
import re
from typing import List, Optional, Callable, Protocol, Annotated

from fastapi import HTTPException, Request, Depends
from starlette.authentication import AuthenticationError
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from fixpoint.errors import UnauthorizedError
from .auth_info import AuthnInfo, new_no_authed_info
from .checkers import AuthChecker


_DEFAULT_HEADER_NAMES = ["api-key", "x-api-key"]
_SCOPE_FIXPOINT_AUTH_INFO = "fixpoint_auth_info"


class _AuthCheckResult(enum.Enum):
    VALID = enum.auto()
    INVALID = enum.auto()
    SKIPPED = enum.auto()


@dataclass
class _AuthCheckWithInfo:
    auth_result: _AuthCheckResult
    auth_info: Optional[AuthnInfo]
    error_msg: Optional[str] = None


class Authenticator(Protocol):
    """
    An Authenticator is responsible for authenticating a request.
    """

    async def authenticate(self, conn: HTTPConnection) -> AuthnInfo:
        """
        Authenticate a request using the provided API key.

        If the request is authenticated, the authenticated user information is
        returned. If the request is not authenticated, an AuthenticationError is
        raised.
        """


class SkipAuthenticator(Authenticator):
    """
    The authenticator that always returns None.
    """

    async def authenticate(self, conn: HTTPConnection) -> AuthnInfo:
        return new_no_authed_info()


class HeaderAuthenticator(Authenticator):
    """
    The authenticator that runs auth checks against API keys from approved API
    key headers.
    """

    _header_names: List[str]
    _additional_headers: List[str]
    _auth_checker: AuthChecker

    def __init__(
        self,
        auth_checker: AuthChecker,
        header_names: Optional[List[str]] = None,
        additional_headers: Optional[List[str]] = None,
    ):
        if header_names is None:
            header_names = list(_DEFAULT_HEADER_NAMES)
        if len(header_names) == 0:
            raise ValueError("Must provide at least one header name")
        self._header_names = header_names
        self._auth_checker = auth_checker
        self._additional_headers = additional_headers or []

    async def authenticate(self, conn: HTTPConnection) -> AuthnInfo:
        """
        Authenticate a request using the provided API key.

        If the request is authenticated, the authenticated user information is
        returned. If the request is not authenticated, an AuthenticationError is
        raised.
        """

        for header_name in self._header_names:
            auth_res = await self._auth(conn, header_name)
            if auth_res.auth_result == _AuthCheckResult.VALID:
                if auth_res.auth_info is None:
                    raise RuntimeError("auth_info is None")
                return auth_res.auth_info
            if auth_res.auth_result == _AuthCheckResult.INVALID:
                raise AuthenticationError("invalid api key")

        raise AuthenticationError(
            f"Must provide an API key in header: {self._header_names[0]}"
        )

    async def _auth(self, conn: HTTPConnection, header_name: str) -> _AuthCheckWithInfo:
        header = conn.headers.get(header_name)
        additional_headers = {}
        for add_header in self._additional_headers:
            additional_headers[add_header] = conn.headers.get(add_header)
        if header is None:
            return _AuthCheckWithInfo(_AuthCheckResult.SKIPPED, None)

        try:
            auth_res = await self._auth_checker(header, additional_headers)
        except UnauthorizedError as e:
            return _AuthCheckWithInfo(_AuthCheckResult.INVALID, None, error_msg=str(e))
        if auth_res is None:
            return _AuthCheckWithInfo(
                _AuthCheckResult.INVALID, None, error_msg="no auth result"
            )
        return _AuthCheckWithInfo(_AuthCheckResult.VALID, auth_res)


_OnError = Callable[[HTTPConnection, Exception], Response]


class ApiKeyAuthenticationMiddleware:
    """
    Middleware to authenticate requests using an API key.

    If the request is authenticated, the authenticated user information is added
    to the request scope.

    If the request is not authenticated, the middleware will call the on_error
    function to handle the error.

    You can set public paths or public paths regex to bypass authentication for
    certain paths.
    """

    _authenticator: Authenticator
    _app: ASGIApp
    _on_error: _OnError
    public_paths: List[str]
    public_paths_regex: List[str]

    def __init__(
        self,
        app: ASGIApp,
        authenticator: Authenticator,
        public_paths: Optional[List[str]] = None,
        public_paths_regex: Optional[List[str]] = None,
        on_error: Optional[_OnError] = None,
    ) -> None:
        self._app = app
        self._authenticator = authenticator
        self._on_error = on_error if on_error is not None else self._default_on_error
        self.public_paths = [
            path for path in public_paths or [] if path.startswith("/")
        ]
        self.public_paths_regex = [
            path for path in public_paths_regex or [] if path.startswith("^")
        ]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") not in ["http", "websocket"]:
            await self._app(scope, receive, send)
            return

        if scope.get("method") in ("OPTIONS", "options"):
            await self._app(scope, receive, send)
            return

        for path in self.public_paths:
            if path == scope["path"]:
                await self._app(scope, receive, send)
                return

        for path in self.public_paths_regex:
            if re.match(path, scope["path"]):
                await self._app(scope, receive, send)
                return

        conn = HTTPConnection(scope)

        try:
            auth_result = await self._authenticator.authenticate(conn)
        except AuthenticationError as e:
            response = self._on_error(conn, e)
            await response(scope, receive, send)
            return

        if auth_result is None:
            response = self._on_error(conn, AuthenticationError("unauthorized"))
            await response(scope, receive, send)
            return

        if auth_result:
            # Add auth_result to the request scope, first making a copy so we
            # don't leak scope changes upstream.
            scope = dict(scope)
            scope[_SCOPE_FIXPOINT_AUTH_INFO] = auth_result
            await self._app(scope, receive, send)
            return

        # Add auth_result to the request scope, first making a copy so we
        # don't leak scope changes upstream.
        scope = dict(scope)
        scope[_SCOPE_FIXPOINT_AUTH_INFO] = auth_result
        await self._app(scope, receive, send)
        return

    @staticmethod
    def _default_on_error(_conn: HTTPConnection, e: Exception) -> Response:
        return JSONResponse({"detail": str(e)}, status_code=401)


def api_key_authentication_info(request: Request) -> AuthnInfo:
    """The authentication info for the current request.

    You must use this in conjunction with `ApiKeyAuthenticationMiddleware`.
    """
    auth_info = request.scope.get(_SCOPE_FIXPOINT_AUTH_INFO)
    if auth_info is None:
        raise HTTPException(
            status_code=401, detail="Authentication information not found"
        )
    # put this on a separate conditional so type-checker can narrow the type
    if not isinstance(auth_info, AuthnInfo):
        raise HTTPException(
            status_code=401, detail="Authentication information not found"
        )

    return auth_info


AuthInfoDep = Annotated[AuthnInfo, Depends(api_key_authentication_info)]
