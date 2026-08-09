# app/main.py
"""
Application entry point — unchanged except import paths.

The lifespan function, route registration, and health check
are identical to the A2 SQLite version.
Only the import paths changed from 'database' to 'app.database'
because files are now inside the app/ package.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import init_db
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs on startup and shutdown.
    init_db() verifies the Postgres connection is working.
    If it fails, the app refuses to start.
    """
    init_db()
    yield
    # Code after yield runs on shutdown (nothing needed here)


app = FastAPI(
    title="Task API",
    description="Task management API backed by Postgres running in Docker",
    version="3.0.0",
    lifespan=lifespan,
)

# Register all routes from routes.py
app.include_router(router)


@app.get("/")
def health_check():
    """Simple health check to confirm the API is running."""
    return {
        "status":   "running",
        "database": "postgres",
        "storage":  "docker volume",
        "version":  "3.0.0",
    }