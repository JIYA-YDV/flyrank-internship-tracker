from pydantic import BaseModel, Field
from typing import Optional


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.
    
    - title is required and cannot be an empty string
    - done is optional and defaults to False
    
    Field(min_length=1) prevents someone from sending
    {"title": ""} which would create a meaningless task.
    """
    title: str = Field(..., min_length=1, description="Task description")
    done: Optional[bool] = Field(False, description="Completion status")


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    
    All fields are Optional — a client may update just the
    title, just the done flag, or both at the same time.
    
    If a field is None it means 'no change requested'.
    """
    title: Optional[str] = Field(None, min_length=1, description="New task title")
    done: Optional[bool] = Field(None, description="New completion status")


class TaskResponse(BaseModel):
    """
    Schema for data returned to the client.
    
    The client always receives id, title, and done.
    Timestamps are included as bonus information.
    
    Note: SQLite stores booleans as integers (0 or 1).
    Pydantic automatically converts them to True/False
    when building a TaskResponse from a dict.
    """
    id: int
    title: str
    done: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"from_attributes": True}


class StatsResponse(BaseModel):
    """Schema for the /stats endpoint."""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int

class StatsResponse(BaseModel):
    """Schema for the GET /stats endpoint."""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int