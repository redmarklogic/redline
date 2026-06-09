"""Authentication dependencies for the Marker API.

Note: Token *verification* is a v0.1 placeholder (presence-only).
Full SSO-based verification is pending issues #50/#73/#48b.
"""

from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer_scheme = HTTPBearer(auto_error=False)


def require_bearer(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(_bearer_scheme)
    ] = None,
) -> str:
    """Require a Bearer token in the Authorization header.

    Raises HTTP 401 when the header is absent or does not use the Bearer scheme.
    Token *content* is not verified in this placeholder implementation.

    Args:
        credentials: Parsed HTTP authorization credentials, or None when absent.

    Returns:
        The raw token string.

    Raises:
        HTTPException: 401 Unauthorized when Bearer credentials are absent.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
