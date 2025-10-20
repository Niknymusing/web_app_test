"""
Data models for the TODO application.
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


class TodoStatus(str, Enum):
    """Enum for TODO item status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoBase(BaseModel):
    """Base model for TODO items."""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the TODO item")
    description: Optional[str] = Field(None, max_length=1000, description="Detailed description")
    status: TodoStatus = Field(default=TodoStatus.PENDING, description="Current status of the TODO")
    priority: int = Field(default=1, ge=1, le=5, description="Priority level (1-5, 5 being highest)")

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        """Validate that title is not just whitespace."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or just whitespace')
        return v.strip()


class TodoCreate(TodoBase):
    """Model for creating a new TODO item."""
    pass


class TodoUpdate(BaseModel):
    """Model for updating an existing TODO item."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TodoStatus] = None
    priority: Optional[int] = Field(None, ge=1, le=5)

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        """Validate that title is not just whitespace."""
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty or just whitespace')
        return v.strip() if v else v


class TodoResponse(TodoBase):
    """Model for TODO item responses."""
    id: str = Field(..., description="Unique identifier for the TODO item")
    created_at: datetime = Field(..., description="Timestamp when the TODO was created")
    updated_at: datetime = Field(..., description="Timestamp when the TODO was last updated")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "todo-123",
                "title": "Complete FastAPI backend",
                "description": "Implement CRUD operations for TODO application",
                "status": "in_progress",
                "priority": 4,
                "created_at": "2025-10-20T12:00:00",
                "updated_at": "2025-10-20T12:30:00"
            }
        }
    )
