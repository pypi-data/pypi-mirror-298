"""Authentication and authorization information about a user or a request"""

__all__ = ["AuthnInfo", "new_no_authed_info"]

from fixpoint.constants import NO_AUTH_USER_ID, NO_AUTH_ORG_ID, NO_AUTH_AUTH_TOKEN


class AuthnInfo:
    """
    Authentication information about a user
    """

    _user_id: str
    _org_id: str
    _auth_token: str

    def __init__(self, user_id: str, org_id: str, auth_token: str):
        self._user_id = user_id
        self._org_id = org_id
        self._auth_token = auth_token

    def __repr__(self) -> str:
        return f'AuthnInfo(user_id={self._user_id}, org_id={self._org_id}, auth_token="***")'

    def user_id(self) -> str:
        """The user ID of the authenticated user"""
        return self._user_id

    def org_id(self) -> str:
        """The organization ID of the authenticated user"""
        return self._org_id

    def auth_token(self) -> str:
        """The authentication token of the authenticated user"""
        return self._auth_token


def new_no_authed_info() -> AuthnInfo:
    """Create a new authentication information for a user who is not authenticated"""
    return AuthnInfo(
        user_id=NO_AUTH_USER_ID, org_id=NO_AUTH_ORG_ID, auth_token=NO_AUTH_AUTH_TOKEN
    )
