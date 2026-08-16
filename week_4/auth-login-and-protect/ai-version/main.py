"""
Secure REST API using FastAPI with Supabase as the Identity Provider.

Routes:
    POST /auth/signup          - create a new user
    POST /auth/login           - exchange credentials for a session
    POST /auth/logout          - invalidate the current session (protected)
    GET  /protected/profile    - return the verified caller's profile (protected)
    GET  /public/info          - public, unauthenticated endpoint

Run with:
    uvicorn main:app --reload
"""

import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from supabase import Client, create_client

# --------------------------------------------------------------------------
# Environment / Supabase client setup
# --------------------------------------------------------------------------

load_dotenv()

SUPABASE_URL: Optional[str] = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: Optional[str] = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set (add them to a .env file "
        "or export them as environment variables) before starting the app."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --------------------------------------------------------------------------
# App + schemas
# --------------------------------------------------------------------------

app = FastAPI(title="Supabase Auth API", version="1.0.0")


class AuthCredentials(BaseModel):
    email: str
    password: str


# --------------------------------------------------------------------------
# Auth dependency
# --------------------------------------------------------------------------

# auto_error=False lets us control the 401 response/detail message ourselves
# instead of FastAPI's default "Not authenticated" error.
bearer_scheme = HTTPBearer(auto_error=False)


def require_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme),
) -> dict:
    """
    Reusable dependency that enforces a valid Supabase-issued access token.

    - Missing Authorization header -> 401 "Access token required"
    - Token present but invalid/expired -> 401 "Invalid or expired token"
    - Token valid -> returns a dict with id, email, created_at, last_sign_in_at
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required",
        )

    token = credentials.credentials

    try:
        user_response = supabase.auth.get_user(token)
    except Exception:
        # Catches gotrue AuthApiError and any other SDK/network exception
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if user_response is None or user_response.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = user_response.user
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
        "last_sign_in_at": user.last_sign_in_at,
    }


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------


@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: AuthCredentials):
    if len(payload.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long",
        )

    try:
        response = supabase.auth.sign_up(
            {"email": payload.email, "password": payload.password}
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if response.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup failed",
        )

    return {
        "id": response.user.id,
        "email": response.user.email,
        "created_at": response.user.created_at,
    }


@app.post("/auth/login", status_code=status.HTTP_200_OK)
def login(payload: AuthCredentials):
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": payload.email, "password": payload.password}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
        )

    if response.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
        )

    session = response.session
    return {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "token_type": "bearer",
        "expires_in": session.expires_in,
    }


@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: dict = Depends(require_auth)):
    try:
        supabase.auth.sign_out()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Logout failed",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/protected/profile", status_code=status.HTTP_200_OK)
def profile(current_user: dict = Depends(require_auth)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "created_at": current_user["created_at"],
    }


@app.get("/public/info", status_code=status.HTTP_200_OK)
def public_info():
    return {"message": "Welcome stranger! This info is public."}
