"""
In-memory database for TODO items.
In production, replace this with a proper database (PostgreSQL, MongoDB, etc.)
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid
from models import TodoCreate, TodoUpdate, TodoResponse, TodoStatus


class TodoDatabase:
    """In-memory database for managing TODO items."""

    def __init__(self):
        """Initialize the database with an empty dictionary."""
        self._todos: Dict[str, dict] = {}

    def _generate_id(self) -> str:
        """Generate a unique ID for a TODO item."""
        return f"todo-{uuid.uuid4().hex[:8]}"

    def create(self, todo: TodoCreate) -> TodoResponse:
        """
        Create a new TODO item.

        Args:
            todo: TodoCreate object with the TODO data

        Returns:
            TodoResponse object with the created TODO
        """
        todo_id = self._generate_id()
        now = datetime.now(timezone.utc)

        todo_data = {
            "id": todo_id,
            "title": todo.title,
            "description": todo.description,
            "status": todo.status,
            "priority": todo.priority,
            "created_at": now,
            "updated_at": now
        }

        self._todos[todo_id] = todo_data
        return TodoResponse(**todo_data)

    def get(self, todo_id: str) -> Optional[TodoResponse]:
        """
        Retrieve a TODO item by ID.

        Args:
            todo_id: The unique identifier of the TODO item

        Returns:
            TodoResponse object if found, None otherwise
        """
        todo_data = self._todos.get(todo_id)
        return TodoResponse(**todo_data) if todo_data else None

    def get_all(self, status: Optional[TodoStatus] = None, priority: Optional[int] = None) -> List[TodoResponse]:
        """
        Retrieve all TODO items, optionally filtered by status and/or priority.

        Args:
            status: Optional status filter
            priority: Optional priority filter

        Returns:
            List of TodoResponse objects
        """
        todos = list(self._todos.values())

        if status:
            todos = [t for t in todos if t["status"] == status]

        if priority:
            todos = [t for t in todos if t["priority"] == priority]

        # Sort by priority (descending) and then by created_at (ascending)
        todos.sort(key=lambda x: (-x["priority"], x["created_at"]))

        return [TodoResponse(**todo) for todo in todos]

    def update(self, todo_id: str, todo_update: TodoUpdate) -> Optional[TodoResponse]:
        """
        Update an existing TODO item.

        Args:
            todo_id: The unique identifier of the TODO item
            todo_update: TodoUpdate object with the fields to update

        Returns:
            TodoResponse object with updated data if found, None otherwise
        """
        if todo_id not in self._todos:
            return None

        todo_data = self._todos[todo_id]
        update_data = todo_update.model_dump(exclude_unset=True)

        # Update only the fields that were provided
        for field, value in update_data.items():
            if value is not None:
                todo_data[field] = value

        todo_data["updated_at"] = datetime.now(timezone.utc)

        return TodoResponse(**todo_data)

    def delete(self, todo_id: str) -> bool:
        """
        Delete a TODO item.

        Args:
            todo_id: The unique identifier of the TODO item

        Returns:
            True if deleted successfully, False if not found
        """
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False

    def count(self) -> int:
        """
        Get the total count of TODO items.

        Returns:
            Total number of TODO items
        """
        return len(self._todos)


# Global database instance
db = TodoDatabase()
