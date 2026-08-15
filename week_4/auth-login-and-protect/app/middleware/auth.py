# app/middleware/auth.py
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import supabase

bearer_scheme = HTTPBearer(auto_error=False)


def require_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    """
    FastAPI dependency — JWT verification guard.
    Runs before any protected route handler.
    Returns verified user dict as current_user on success.
    Raises 401 on any failure.
    """

    # ── Step 1: Check token presence ────────────────────────────────────────
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required — token is empty",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ── Step 2: Verify token with Supabase ───────────────────────────────────
    try:
        response = supabase.auth.get_user(token)
    except Exception as e:
        # Supabase SDK throws exception for invalid/expired tokens
        # in newer SDK versions instead of returning None
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if response is None or response.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ── Step 3: Safely build user dict ───────────────────────────────────────
    # Use safe extraction — any field can be None in edge cases
    user = response.user
    return {
        "id":              str(user.id) if user.id else None,
        "email":           user.email or None,
        "created_at":      str(user.created_at) if user.created_at else None,
        # last_sign_in_at is None for brand new accounts — handle it
        "last_sign_in_at": str(user.last_sign_in_at) if user.last_sign_in_at else None,
    }