from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Task API",
    description="CRUD API for managing to-do tasks",
    version="1.0"
)

# ── In-memory "database" ──────────────────────────────────────────────────────
# A plain Python list. Fast, simple, and gone when the server stops.
# That impermanence is intentional — it's the lesson Week 3 fixes with a database.

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read FastAPI docs", "done": True},
    {"id": 3, "title": "Push code to GitHub", "done": False},
]

next_id = 4  # tracks the next available id


# ── Utility endpoints ─────────────────────────────────────────────────────────

@app.get("/")
def root():
    """API info."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    """Health check — used by monitoring tools to confirm the server is alive."""
    return {"status": "ok"}


# ── Read endpoints ────────────────────────────────────────────────────────────

@app.get("/tasks")
def list_tasks():
    """Return all tasks."""
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Return a single task by ID. Returns 404 if not found."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")