"""
This module contains authentication checkers that can call out to other
authentication services.
"""

__all__ = ["AuthChecker", "propel_auth_checker"]

import os
from typing import Any, Dict, Optional
from propelauth_py import (
    init_base_auth,
    UnauthorizedException as PropelAuthUnauthorizedException,
    Auth,
)

from fixpoint.types import AsyncFunc
from fixpoint.errors import UnauthorizedError
from .auth_info import AuthnInfo


class PropelAuthState:
    """
    This class is used to store the PropelAuth state.
    """

    auth: Optional[Auth] = None

    @classmethod
    def get_auth(cls) -> Auth:
        """
        This method retrieves the PropelAuth state.
        """
        if cls.auth is None:
            auth_url = os.environ["PROPELAUTH_AUTH_URL"]
            api_key = os.environ["PROPELAUTH_API_KEY"]
            cls.auth = init_base_auth(auth_url, api_key)
        return cls.auth


# Takes the API key, and returns True if the key is valid, False otherwise.
AuthChecker = AsyncFunc[[str, Dict[str, Any]], Optional[AuthnInfo]]


async def propel_auth_checker(
    api_key: str, additional_headers: Dict[str, str]
) -> AuthnInfo:
    """Authenticate with PropelAuth"""
    auth = PropelAuthState.get_auth()
    org_id = additional_headers.get("x-org-id")
    try:
        return _validate_from_access_token(auth, api_key, org_id)
    except UnauthorizedError as e1:
        try:
            return _validate_from_api_key(auth, api_key, org_id)
        except UnauthorizedError as e2:
            # TODO(dbmikus) should we raise e1 or e2?
            raise e1 from e2


def _validate_from_access_token(
    auth: Auth, api_key: str, org_id: Optional[str]
) -> AuthnInfo:
    """Validates an access token

    Validates an access JWT token. This is for requests that come from the
    frontend. This is not the same as validating an opaque API key.
    """
    try:
        user = auth.validate_access_token_and_get_user(api_key)
    except PropelAuthUnauthorizedException as e:
        raise UnauthorizedError(str(e)) from e
    if org_id is None or org_id == "personal":
        # TODO(dbmikus) should we check if the API key belongs to an org, or
        # just assume it's personal unless they specify an org?
        org_id = f"org-user:{user.user_id}"
    else:
        # If the org is not personal, check that the user has access to org
        org = user.get_org(org_id)
        if org is None:
            raise UnauthorizedError("Invalid organization")
        org_id = f"org-{org_id}"
    return AuthnInfo(user_id=user.user_id, org_id=org_id, auth_token=api_key)


def _validate_from_api_key(
    auth: Auth, api_key: str, org_id: Optional[str]
) -> AuthnInfo:
    """Validates an API key

    Validates an API key. This is for requests that come from the backend. This is
    not the same as validating an access JWT token.
    """
    try:
        auth_resp: Dict[str, Any] = auth.validate_api_key(api_key)
    except PropelAuthUnauthorizedException as e:
        raise UnauthorizedError(str(e)) from e
    return validate_api_key_response(api_key, org_id, auth_resp)


def validate_api_key_response(
    api_key: str, org_id: Optional[str], auth_resp: Dict[str, Any]
) -> AuthnInfo:
    """Validate an API key response from PropelAuth.

    Validate an API key response from PropelAuth, making sure that we have an
    authorized user and/or organization that matches the data for the PropelAuth
    API key.
    """
    fetched_user_id: Optional[str] = auth_resp.get("user_id")
    fetched_org_id: Optional[str] = auth_resp.get("org_id")
    if org_id is None or org_id == "personal":
        if fetched_user_id is None:
            raise UnauthorizedError(
                "API key is not tied to a user. Please specify an organization."
            )
        # TODO(dbmikus) should we check if the API key belongs to an org, or
        # just assume it's personal unless they specify an org?
        org_id = f"org-user:{fetched_user_id}"
    else:
        # If the org is not personal, check that the user has access to org
        if fetched_org_id is None:
            raise UnauthorizedError("API key is not tied to an organization")
        if org_id != fetched_org_id:
            raise UnauthorizedError(
                "API key's organization does not match specified organization"
            )
        org_id = f"org-{org_id}"

    if not fetched_user_id and not fetched_org_id:
        raise UnauthorizedError("API key is not tied to a user or organization")
    if not fetched_user_id:
        user_id = f"user-org:{fetched_org_id}"
    else:
        user_id = f"user-{fetched_user_id}"

    return AuthnInfo(user_id=user_id, org_id=org_id, auth_token=api_key)
