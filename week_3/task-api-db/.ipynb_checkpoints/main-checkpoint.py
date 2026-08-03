from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import init_db
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager — runs once when the server starts.

    This is the modern FastAPI way to run startup code.
    
    What happens at startup:
        1. create_table() — creates tasks table if missing
        2. seed_tasks()   — inserts 3 tasks if table is empty

    The `yield` separates startup from shutdown code.
    Code after yield runs when the server shuts down.
    """
    print("🚀 Starting Task API...")
    init_db()
    yield
    print("🛑 Server shutting down.")


app = FastAPI(
    title="Task Management API",
    description=(
        "A RESTful CRUD API backed by SQLite. "
        "Built for Week 3 of the FlyRank AI Backend Engineering track."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

# Register all routes from routes.py
app.include_router(router)


@app.get("/")
def root():
    """
    Health check — confirms the server is running.
    Visit http://localhost:8000/docs for interactive API docs.
    """
    return {
        "status": "running",
        "message": "Task API with SQLite persistence is live ✅",
        "docs": "http://localhost:8000/docs"
    }