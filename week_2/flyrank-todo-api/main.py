from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

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

# ── Request models ────────────────────────────────────────────────────────────

class TaskCreate(BaseModel):
    title: str = Field(..., description="Text of the task", example="Buy milk")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("title must not be empty or whitespace")
        return v.strip()

# ── Create endpoint ───────────────────────────────────────────────────────────

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    """Create a new task. Returns 201 with the created task."""
    global next_id
    new_task = {
        "id": next_id,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    next_id += 1
    return new_task

class TaskUpdate(BaseModel):
    title: str | None = Field(None, description="New title for the task", example="Buy oat milk")
    done: bool | None = Field(None, description="Mark task complete or incomplete", example=True)

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("title must not be empty or whitespace")
        return v.strip() if v else v

# ── Update endpoint ───────────────────────────────────────────────────────────

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    """Update title and/or done status. Returns 404 if not found, 400 if body is empty."""
    if update.title is None and update.done is None:
        raise HTTPException(
            status_code=400,
            detail="Request body must include at least one of: title, done"
        )
    for task in tasks:
        if task["id"] == task_id:
            if update.title is not None:
                task["title"] = update.title
            if update.done is not None:
                task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ── Delete endpoint ───────────────────────────────────────────────────────────

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task. Returns 204 No Content on success, 404 if not found."""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return  # 204 = empty body, return nothing
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

  