# app/main.py
# FastAPI application entry point.
# Registers all routers and configures the app metadata that
# FastAPI uses to auto-generate the Swagger UI at /docs.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers (we will fill these out in stages 1–4)
from app.routes import auth, protected, public

# ── App metadata ──────────────────────────────────────────────────────────────
# FastAPI uses this to build the Swagger /docs page automatically.
# The openapi_tags list creates sections in the Swagger UI sidebar.
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
    openapi_tags=[
        {"name": "Public",         "description": "Open endpoints — no token needed"},
        {"name": "Authentication", "description": "Sign up, log in, log out"},
        {"name": "Protected",      "description": "🔒 Requires a valid Bearer token"},
    ],
)

# ── CORS ──────────────────────────────────────────────────────────────────────
# Allows browsers to call the API from any origin during development.
# In production you would restrict this to your frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(public.router,    prefix="/public",    tags=["Public"])
app.include_router(auth.router,      prefix="/auth",      tags=["Authentication"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])

# ── Root health check ─────────────────────────────────────────────────────────
@app.get("/", tags=["Public"])
def root():
    return {
        "message": "FlyRank Auth API is running 🚀",
        "docs": "/docs",
        "version": "1.0.0",
    }