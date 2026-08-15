# app/routes/public.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/info")
def public_info():
    """Open endpoint — no token needed."""
    return {
        "message": "Welcome stranger! This info is public.",
        "description": "FlyRank Auth API — no token needed to read this.",
        "available_endpoints": {
            "signup":    "POST /auth/signup",
            "login":     "POST /auth/login",
            "logout":    "POST /auth/logout  (requires token)",
            "profile":   "GET  /protected/profile  (requires token)",
            "dashboard": "GET  /protected/dashboard (requires token)",
        },
        "docs": "http://localhost:8000/docs",
    }