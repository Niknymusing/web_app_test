"""
FastAPI backend for TODO application.
Provides RESTful API endpoints for CRUD operations on TODO items.
"""
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import TodoCreate, TodoUpdate, TodoResponse, TodoStatus
from database import db

# Initialize FastAPI app
app = FastAPI(
    title="TODO API",
    description="A RESTful API for managing TODO items with full CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "TODO API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "todos": "/todos"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "total_todos": db.count()
    }


@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["TODOs"],
    summary="Create a new TODO item"
)
async def create_todo(todo: TodoCreate):
    """
    Create a new TODO item with the provided data.

    - **title**: Required, 1-200 characters
    - **description**: Optional, up to 1000 characters
    - **status**: Default is 'pending', can be 'pending', 'in_progress', or 'completed'
    - **priority**: Default is 1, range 1-5 (5 being highest)
    """
    try:
        new_todo = db.create(todo)
        return new_todo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create TODO: {str(e)}"
        )


@app.get(
    "/todos",
    response_model=List[TodoResponse],
    tags=["TODOs"],
    summary="Get all TODO items"
)
async def get_todos(
    status_filter: Optional[TodoStatus] = Query(None, alias="status", description="Filter by status"),
    priority: Optional[int] = Query(None, ge=1, le=5, description="Filter by priority")
):
    """
    Retrieve all TODO items, optionally filtered by status and/or priority.

    Results are sorted by priority (descending) and creation date (ascending).
    """
    try:
        todos = db.get_all(status=status_filter, priority=priority)
        return todos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve TODOs: {str(e)}"
        )


@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    tags=["TODOs"],
    summary="Get a specific TODO item"
)
async def get_todo(todo_id: str):
    """
    Retrieve a specific TODO item by its unique identifier.
    """
    todo = db.get(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO item with id '{todo_id}' not found"
        )
    return todo


@app.put(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    tags=["TODOs"],
    summary="Update a TODO item"
)
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    """
    Update an existing TODO item. Only provided fields will be updated.

    All fields are optional:
    - **title**: 1-200 characters
    - **description**: Up to 1000 characters
    - **status**: 'pending', 'in_progress', or 'completed'
    - **priority**: Range 1-5
    """
    updated_todo = db.update(todo_id, todo_update)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO item with id '{todo_id}' not found"
        )
    return updated_todo


@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["TODOs"],
    summary="Delete a TODO item"
)
async def delete_todo(todo_id: str):
    """
    Delete a specific TODO item by its unique identifier.
    """
    deleted = db.delete(todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO item with id '{todo_id}' not found"
        )
    return None


@app.get(
    "/todos/stats/summary",
    tags=["Statistics"],
    summary="Get TODO statistics"
)
async def get_stats():
    """
    Get statistics about TODO items including counts by status and priority distribution.
    """
    all_todos = db.get_all()

    stats = {
        "total": len(all_todos),
        "by_status": {
            "pending": len([t for t in all_todos if t.status == TodoStatus.PENDING]),
            "in_progress": len([t for t in all_todos if t.status == TodoStatus.IN_PROGRESS]),
            "completed": len([t for t in all_todos if t.status == TodoStatus.COMPLETED])
        },
        "by_priority": {}
    }

    for priority in range(1, 6):
        stats["by_priority"][str(priority)] = len([t for t in all_todos if t.priority == priority])

    return stats


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
