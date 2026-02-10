from __future__ import annotations

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.firebase import verify_firebase_id_token
from app.models.auth import AuthenticatedUser

bearer_auth = HTTPBearer(auto_error=False)


def require_authenticated_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_auth),
) -> AuthenticatedUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer token",
        )

    claims = verify_firebase_id_token(credentials.credentials)
    uid = claims.get("uid") or claims.get("sub")
    if not uid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing uid claim")

    return AuthenticatedUser(uid=str(uid), email=claims.get("email"))


def require_authenticated_uid(user: AuthenticatedUser = Depends(require_authenticated_user)) -> str:
    return user.uid
