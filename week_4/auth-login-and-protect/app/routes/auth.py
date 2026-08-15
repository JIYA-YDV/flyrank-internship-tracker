# app/routes/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from app.config import supabase
from app.middleware.auth import require_auth

router = APIRouter()


class AuthCredentials(BaseModel):
    email: EmailStr
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
    refresh_token: str


# ── POST /auth/signup ─────────────────────────────────────────────────────────
@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new account",
)
def signup(credentials: AuthCredentials):
    """
    Creates a new user account via Supabase Auth.
    Supabase hashes the password — we never see or store it.
    """

    if len(credentials.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters",
        )

    try:
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password,
        })
    except Exception as e:
        # Catch any Supabase SDK exception and return readable error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Signup failed: {str(e)}",
        )

    if response.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup failed — email may already be registered",
        )

    # Safely extract fields — use getattr with defaults to avoid None crashes
    return {
        "message": "Account created successfully",
        "user": {
            "id":         str(response.user.id) if response.user.id else None,
            "email":      response.user.email,
            "created_at": str(response.user.created_at) if response.user.created_at else None,
        },
    }


# ── POST /auth/login ──────────────────────────────────────────────────────────
@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Log in and get a JWT",
)
def login(credentials: AuthCredentials):
    """
    Authenticates the user and returns a JWT access token.
    Copy the access_token and use it in the Authorize button above.
    """

    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password,
        })
    except Exception as e:
        # Supabase throws an exception for wrong credentials in some SDK versions
        # Catch it and return a clean 401
        error_msg = str(e).lower()
        if "invalid" in error_msg or "credentials" in error_msg or "password" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login credentials",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}",
        )

    # Check session exists
    if response.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
        )

    session = response.session
    user    = response.user

    # Safely extract all fields — avoid None serialization crashes
    # expires_in can be None in some SDK versions
    return {
        "message":       "Login successful",
        "access_token":  session.access_token,
        "refresh_token": session.refresh_token,
        "token_type":    "Bearer",
        "expires_in":    session.expires_in if session.expires_in is not None else 3600,
        "user": {
            "id":    str(user.id) if user and user.id else None,
            "email": user.email  if user else None,
        },
    }


# ── POST /auth/logout ─────────────────────────────────────────────────────────
@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Log out",
)
def logout(current_user: dict = Depends(require_auth)):
    """
    Ends the session. Returns 204 No Content.
    Note: access token stays valid until expiry (~1hr) — JWTs are stateless.
    """
    try:
        supabase.auth.sign_out()
    except Exception:
        # Even if signout fails on Supabase side, treat as success
        # The client should discard the token regardless
        pass
    # Return nothing — FastAPI sends 204 automatically


# ── POST /auth/refresh ────────────────────────────────────────────────────────
@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
)
def refresh_token(body: RefreshRequest):
    """
    Exchange a refresh token for a new access token.
    Access tokens are short-lived (~1hr) to limit damage if stolen.
    """
    try:
        response = supabase.auth.refresh_session(body.refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Refresh failed: {str(e)}",
        )

    if response.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token — please log in again",
        )

    return {
        "message":       "Token refreshed successfully",
        "access_token":  response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "expires_in":    response.session.expires_in if response.session.expires_in is not None else 3600,
    }