# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, protected, public

app = FastAPI(
    title="FlyRank Auth API",
    description=(
        "Secure authentication API built with **FastAPI** and **Supabase Auth**.\n\n"
        "## How to use protected routes\n"
        "1. Call `POST /auth/login` with your credentials\n"
        "2. Copy the `access_token` from the response\n"
        "3. Click the **Authorize 🔒** button at the top of this page\n"
        "4. Paste your token and click Authorize\n"
        "5. All 🔒 routes will now include your token automatically"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Public",
            "description": "Open endpoints — no token needed.",
        },
        {
            "name": "Authentication",
            "description": "Sign up, log in, log out. Login returns the access_token.",
        },
        {
            "name": "Protected",
            "description": "🔒 Requires Bearer token. Click Authorize above.",
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public.router,    prefix="/public",    tags=["Public"])
app.include_router(auth.router,      prefix="/auth",      tags=["Authentication"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])


@app.get("/", tags=["Public"], summary="Health check")
def root():
    """API health check — confirms the server is running."""
    return {
        "message": "FlyRank Auth API is running",
        "docs":    "http://localhost:8000/docs",
        "version": "1.0.0",
    }