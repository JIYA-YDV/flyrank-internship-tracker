# app/main.py
"""
Application entry point — unchanged except import paths.

The lifespan function, route registration, and health check
are identical to the A2 SQLite version.
Only the import paths changed from 'database' to 'app.database'
because files are now inside the app/ package.
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
import redis as redis_lib

from app.database import init_db
from app.routes import router


def ping_redis():
  """Verify Redis connection on startup."""
  try:
    r = redis_lib.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))
    r.ping()
    print("✅ Redis connection verified")
  except Exception as e:
    print(f"⚠️  Redis not available: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
  """Runs on startup and shutdown.

  init_db() verifies the Postgres connection is working.
  If it fails, the app refuses to start.
  """
  init_db()
  ping_redis()
  yield
  # Code after yield runs on shutdown (nothing needed here)


app = FastAPI(
    title="Task API",
    description="Task management API backed by Postgres running in Docker",
    version="3.0.0",
    lifespan=lifespan,
)


@app.get("/redis-ping")
def redis_ping_route():
  try:
    r = redis_lib.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))
    response = r.ping()
    return {"redis_status": "connected", "ping": response}
  except Exception as e:
    return {"redis_status": "failed", "error": str(e)}


# Register all routes from routes.py
app.include_router(router)


@app.get("/")
def health_check():
  """Simple health check to confirm the API is running."""
  return {
      "status": "running",
      "database": "postgres",
      "storage": "docker volume",
      "version": "3.0.0",
  }