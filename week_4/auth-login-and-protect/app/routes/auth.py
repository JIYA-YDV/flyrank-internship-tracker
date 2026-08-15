# app/routes/auth.py
# Authentication endpoints — signup, login, logout.
# We never store passwords or hash anything ourselves.
# Supabase receives credentials and handles everything cryptographic.

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from app.config import supabase
from app.middleware.auth import require_auth

router = APIRouter()


# ── Request body models ───────────────────────────────────────────────────────
# Pydantic validates incoming JSON automatically.
# Wrong type or missing field → FastAPI returns 422 before our code runs.

class AuthCredentials(BaseModel):
    """Body expected by /signup and /login."""
    email: EmailStr   # Pydantic validates email format
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "test@example.com",
                "password": "password123",
            }
        }
    }


class RefreshRequest(BaseModel):
    """Body expected by /refresh."""
    refresh_token: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "refresh_token": "your-refresh-token-here"
            }
        }
    }


# ── POST /auth/signup ─────────────────────────────────────────────────────────
@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new account",
    description=(
        "Registers a new user with Supabase Auth. "
        "Supabase hashes the password — your server never sees or stores it."
    ),
)
def signup(credentials: AuthCredentials):
    """
    Creates a new user account.

    Returns the new user id, email, and creation timestamp.
    Returns **400** if the email is already registered or password too short.
    """

    # Fast-fail on short password before hitting Supabase
    if len(credentials.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters",
        )

    # sign_up() sends credentials to Supabase which:
    #   • checks for duplicate emails
    #   • hashes the password with bcrypt (we never see the hash)
    #   • creates the account
    response = supabase.auth.sign_up({
        "email": credentials.email,
        "password": credentials.password,
    })

    if response.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup failed — email may already be registered",
        )

    return {
        "message": "Account created successfully",
        "user": {
            "id":         str(response.user.id),
            "email":      response.user.email,
            "created_at": str(response.user.created_at),
        },
    }


# ── POST /auth/login ──────────────────────────────────────────────────────────
@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Log in and get a JWT",
    description=(
        "Authenticates the user and returns an **access token** (JWT). "
        "Copy the `access_token` and paste it into the **Authorize 🔒** button above."
    ),
)
def login(credentials: AuthCredentials):
    """
    Verifies credentials and returns a JWT.

    - **access_token**: short-lived JWT (~1 hour) — send in Authorization header
    - **refresh_token**: long-lived — use /auth/refresh to get a new access token
    """
    response = supabase.auth.sign_in_with_password({
        "email": credentials.email,
        "password": credentials.password,
    })

    if response.session is None:
        # Always 401 for bad credentials.
        # Never reveal which field was wrong — that helps attackers
        # confirm which emails are registered (user enumeration attack).
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
        )

    session = response.session

    return {
        "message":       "Login successful",
        "access_token":  session.access_token,
        "refresh_token": session.refresh_token,
        "token_type":    "Bearer",
        "expires_in":    session.expires_in,
        "user": {
            "id":    str(response.user.id),
            "email": response.user.email,
        },
    }


# ── POST /auth/logout ─────────────────────────────────────────────────────────
@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Log out",
    description=(
        "Ends the user session. **Requires** a valid Bearer token.\n\n"
        "Note: the access token remains valid until expiry (~1 hour) "
        "because JWTs are stateless. sign_out() revokes the refresh token "
        "so the session cannot be renewed."
    ),
)
def logout(current_user: dict = Depends(require_auth)):
    """
    Ends the session by revoking the refresh token on Supabase.
    Returns 204 No Content on success.
    """
    supabase.auth.sign_out()
    # FastAPI automatically returns an empty 204 response
    # Do not return anything here — FastAPI will error if you do


# ── POST /auth/refresh ────────────────────────────────────────────────────────
@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description=(
        "Exchange a **refresh token** for a new access token.\n\n"
        "Access tokens are short-lived (~1 hour) to limit damage if stolen. "
        "The refresh token lets the client renew silently without re-login."
    ),
)
def refresh_token(body: RefreshRequest):
    """
    Why access tokens are short-lived:
    If stolen, the window of damage is only ~1 hour.
    The refresh token is long-lived but transmitted much less often.
    """
    response = supabase.auth.refresh_session(body.refresh_token)

    if response.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token — please log in again",
        )

    return {
        "message":       "Token refreshed successfully",
        "access_token":  response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "expires_in":    response.session.expires_in,
    }