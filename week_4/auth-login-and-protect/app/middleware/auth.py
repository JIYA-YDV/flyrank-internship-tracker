# app/middleware/auth.py
# The single reusable auth guard for the entire API.
# Any route that declares Depends(require_auth) will run this first.

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import supabase

# HTTPBearer does two things:
#   1. Parses the Authorization: Bearer <token> header for us
#   2. Makes the lock icon appear in Swagger UI automatically
# auto_error=False means WE control the 401 error message
bearer_scheme = HTTPBearer(auto_error=False)


def require_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    """
    FastAPI dependency — JWT verification guard.

    Steps:
      1. Check Authorization header exists and has a token
      2. Call supabase.auth.get_user(token) — real network verification
      3. If invalid → raise 401 (route body never runs)
      4. If valid   → return verified user dict as current_user

    Apply to any route:
        current_user: dict = Depends(require_auth)
    """

    # ── Step 1: Check token presence ────────────────────────────────────────
    # credentials is None when Authorization header is completely missing
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # credentials.credentials is the raw JWT string after "Bearer "
    token = credentials.credentials

    # Catch edge case: "Authorization: Bearer " with nothing after the space
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required — token is empty",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ── Step 2: Verify token with Supabase ───────────────────────────────────
    # get_user() makes a real network call to Supabase.
    # Supabase checks:
    #   • Cryptographic signature — was this token really issued by us?
    #   • Expiry timestamp        — is it still within the valid window?
    #   • Session status          — has it been revoked?
    # This is why we use get_user() instead of decoding locally —
    # local decoding cannot detect revoked sessions.
    try:
        response = supabase.auth.get_user(token)
    except Exception:
        # Network error or unexpected Supabase failure
        # Never leak internal error details to the client
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed — please log in again",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # response.user is None when token is expired or tampered
    if response is None or response.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ── Step 3: Return verified user dict ────────────────────────────────────
    # This becomes `current_user` in every protected route handler.
    # All data here came from Supabase — never trust client-supplied IDs.
    user = response.user
    return {
        "id":              str(user.id),
        "email":           user.email,
        "created_at":      str(user.created_at),
        "last_sign_in_at": str(user.last_sign_in_at),
    }