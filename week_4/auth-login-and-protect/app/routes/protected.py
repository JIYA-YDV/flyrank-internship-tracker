# app/routes/protected.py
# Routes that require authentication.
# require_auth runs BEFORE each handler via Depends().
# If the token is missing or invalid, the handler body never executes.

from fastapi import APIRouter, Depends, HTTPException, status
from app.middleware.auth import require_auth

router = APIRouter()

# Hardcoded admin email for the 403 demo
# In production this would be a role column in your database
ADMIN_EMAIL = "admin@flyrank.io"


# ── GET /protected/profile ────────────────────────────────────────────────────
@router.get(
    "/profile",
    summary="Get your private profile",
    description=(
        "🔒 Returns the authenticated user's profile data.\n\n"
        "Requires a valid Bearer token in the Authorization header."
    ),
)
def get_profile(current_user: dict = Depends(require_auth)):
    """
    Private profile endpoint.

    `require_auth` runs first and verifies the JWT with Supabase.
    `current_user` contains server-verified data — never trust client input.
    """
    return {
        "message": "Welcome to your private profile",
        "user": {
            "id":              current_user["id"],
            "email":           current_user["email"],
            "created_at":      current_user["created_at"],
            "last_sign_in_at": current_user["last_sign_in_at"],
        },
    }


# ── GET /protected/dashboard ──────────────────────────────────────────────────
@router.get(
    "/dashboard",
    summary="Get your private dashboard",
    description=(
        "🔒 Returns private dashboard stats.\n\n"
        "Uses the **same** `require_auth` dependency as /profile — "
        "no new auth code written. This proves middleware reuse."
    ),
)
def get_dashboard(current_user: dict = Depends(require_auth)):
    """
    Private dashboard — demonstrates Depends() reuse.
    Same guard as profile, zero duplicated auth logic.
    """
    return {
        "message": f"Welcome to your dashboard, {current_user['email']}",
        "user_id": current_user["id"],
        "stats": {
            "audits_run":        42,
            "keywords_tracked":  150,
            "rank_improvements": 18,
        },
        "note": "This data is private — only you can see it",
    }


# ── GET /protected/admin ──────────────────────────────────────────────────────
# Demonstrates the 401 vs 403 distinction:
#   401 Unauthorized = "I don't know who you are" — handled by require_auth
#   403 Forbidden    = "I know exactly who you are — and still no"
@router.get(
    "/admin",
    summary="Admin only — demonstrates 403 Forbidden",
    description=(
        "🔒 Requires token **and** admin role.\n\n"
        "- `401` = no/bad token → handled by `require_auth` before this runs\n"
        "- `403` = valid token, but you are not an admin → this route\n\n"
        "**401** asks *'who are you?'*  |  **403** says *'I know you, and no.'*"
    ),
)
def admin_only(current_user: dict = Depends(require_auth)):
    """
    401 vs 403 explained:
    - 401: Authentication failed — we don't know who the caller is
    - 403: Authorization failed — we know who they are, they just aren't allowed
    """
    # At this point require_auth already passed → user IS authenticated
    # Now we check AUTHORIZATION — are they ALLOWED to do this specific thing?
    if current_user["email"] != ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"Access denied. Admin privileges required. "
                f"You are authenticated as '{current_user['email']}' "
                f"but this route requires admin role."
            ),
        )

    return {
        "message": "Welcome, admin! You have full access.",
        "admin_data": {
            "total_users":   1204,
            "active_audits": 87,
        },
    }