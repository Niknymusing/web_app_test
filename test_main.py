"""
Comprehensive tests for the TODO API.
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from database import db
from models import TodoStatus


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the database before each test."""
    db._todos.clear()
    yield
    db._todos.clear()


class TestRootEndpoints:
    """Tests for root and health endpoints."""

    def test_root_endpoint(self, client):
        """Test the root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "total_todos" in data


class TestCreateTodo:
    """Tests for creating TODO items."""

    def test_create_todo_minimal(self, client):
        """Test creating a TODO with minimal required fields."""
        todo_data = {
            "title": "Test TODO"
        }
        response = client.post("/todos", json=todo_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test TODO"
        assert data["status"] == "pending"
        assert data["priority"] == 1
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_todo_full(self, client):
        """Test creating a TODO with all fields."""
        todo_data = {
            "title": "Complete project",
            "description": "Finish the FastAPI backend",
            "status": "in_progress",
            "priority": 5
        }
        response = client.post("/todos", json=todo_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Complete project"
        assert data["description"] == "Finish the FastAPI backend"
        assert data["status"] == "in_progress"
        assert data["priority"] == 5

    def test_create_todo_empty_title(self, client):
        """Test that creating a TODO with empty title fails."""
        todo_data = {
            "title": ""
        }
        response = client.post("/todos", json=todo_data)
        assert response.status_code == 422

    def test_create_todo_whitespace_title(self, client):
        """Test that creating a TODO with whitespace-only title fails."""
        todo_data = {
            "title": "   "
        }
        response = client.post("/todos", json=todo_data)
        assert response.status_code == 422

    def test_create_todo_invalid_priority(self, client):
        """Test that invalid priority values are rejected."""
        todo_data = {
            "title": "Test",
            "priority": 10
        }
        response = client.post("/todos", json=todo_data)
        assert response.status_code == 422

    def test_create_todo_title_too_long(self, client):
        """Test that titles exceeding max length are rejected."""
        todo_data = {
            "title": "x" * 201
        }
        response = client.post("/todos", json=todo_data)
        assert response.status_code == 422


class TestGetTodos:
    """Tests for retrieving TODO items."""

    def test_get_all_todos_empty(self, client):
        """Test getting all TODOs when database is empty."""
        response = client.get("/todos")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_todos(self, client):
        """Test getting all TODOs."""
        # Create multiple TODOs
        client.post("/todos", json={"title": "TODO 1", "priority": 3})
        client.post("/todos", json={"title": "TODO 2", "priority": 5})
        client.post("/todos", json={"title": "TODO 3", "priority": 1})

        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        # Should be sorted by priority descending
        assert data[0]["priority"] == 5
        assert data[1]["priority"] == 3
        assert data[2]["priority"] == 1

    def test_get_todos_filter_by_status(self, client):
        """Test filtering TODOs by status."""
        client.post("/todos", json={"title": "TODO 1", "status": "pending"})
        client.post("/todos", json={"title": "TODO 2", "status": "in_progress"})
        client.post("/todos", json={"title": "TODO 3", "status": "completed"})

        response = client.get("/todos?status=in_progress")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "in_progress"

    def test_get_todos_filter_by_priority(self, client):
        """Test filtering TODOs by priority."""
        client.post("/todos", json={"title": "TODO 1", "priority": 1})
        client.post("/todos", json={"title": "TODO 2", "priority": 3})
        client.post("/todos", json={"title": "TODO 3", "priority": 3})

        response = client.get("/todos?priority=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(todo["priority"] == 3 for todo in data)


class TestGetSingleTodo:
    """Tests for retrieving a single TODO item."""

    def test_get_todo_success(self, client):
        """Test getting a specific TODO by ID."""
        create_response = client.post("/todos", json={"title": "Test TODO"})
        todo_id = create_response.json()["id"]

        response = client.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Test TODO"

    def test_get_todo_not_found(self, client):
        """Test getting a non-existent TODO."""
        response = client.get("/todos/nonexistent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateTodo:
    """Tests for updating TODO items."""

    def test_update_todo_title(self, client):
        """Test updating only the title."""
        create_response = client.post("/todos", json={"title": "Original Title"})
        todo_id = create_response.json()["id"]

        update_response = client.put(
            f"/todos/{todo_id}",
            json={"title": "Updated Title"}
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["title"] == "Updated Title"

    def test_update_todo_status(self, client):
        """Test updating the status."""
        create_response = client.post("/todos", json={"title": "Test"})
        todo_id = create_response.json()["id"]

        update_response = client.put(
            f"/todos/{todo_id}",
            json={"status": "completed"}
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["status"] == "completed"

    def test_update_todo_multiple_fields(self, client):
        """Test updating multiple fields at once."""
        create_response = client.post("/todos", json={"title": "Test", "priority": 1})
        todo_id = create_response.json()["id"]

        update_response = client.put(
            f"/todos/{todo_id}",
            json={
                "title": "Updated",
                "description": "New description",
                "priority": 5,
                "status": "in_progress"
            }
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["title"] == "Updated"
        assert data["description"] == "New description"
        assert data["priority"] == 5
        assert data["status"] == "in_progress"

    def test_update_todo_not_found(self, client):
        """Test updating a non-existent TODO."""
        response = client.put(
            "/todos/nonexistent-id",
            json={"title": "Updated"}
        )
        assert response.status_code == 404

    def test_update_todo_empty_title(self, client):
        """Test that updating with empty title fails."""
        create_response = client.post("/todos", json={"title": "Test"})
        todo_id = create_response.json()["id"]

        update_response = client.put(
            f"/todos/{todo_id}",
            json={"title": ""}
        )
        assert update_response.status_code == 422


class TestDeleteTodo:
    """Tests for deleting TODO items."""

    def test_delete_todo_success(self, client):
        """Test successfully deleting a TODO."""
        create_response = client.post("/todos", json={"title": "To Delete"})
        todo_id = create_response.json()["id"]

        delete_response = client.delete(f"/todos/{todo_id}")
        assert delete_response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404

    def test_delete_todo_not_found(self, client):
        """Test deleting a non-existent TODO."""
        response = client.delete("/todos/nonexistent-id")
        assert response.status_code == 404


class TestStatistics:
    """Tests for statistics endpoint."""

    def test_get_stats_empty(self, client):
        """Test statistics when database is empty."""
        response = client.get("/todos/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0

    def test_get_stats_with_data(self, client):
        """Test statistics with various TODOs."""
        client.post("/todos", json={"title": "T1", "status": "pending", "priority": 1})
        client.post("/todos", json={"title": "T2", "status": "in_progress", "priority": 3})
        client.post("/todos", json={"title": "T3", "status": "completed", "priority": 5})
        client.post("/todos", json={"title": "T4", "status": "pending", "priority": 1})

        response = client.get("/todos/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 4
        assert data["by_status"]["pending"] == 2
        assert data["by_status"]["in_progress"] == 1
        assert data["by_status"]["completed"] == 1
        assert data["by_priority"]["1"] == 2
        assert data["by_priority"]["3"] == 1
        assert data["by_priority"]["5"] == 1


class TestIntegrationScenarios:
    """Integration tests for real-world scenarios."""

    def test_complete_workflow(self, client):
        """Test a complete CRUD workflow."""
        # Create
        create_response = client.post("/todos", json={
            "title": "Learn FastAPI",
            "priority": 4
        })
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]

        # Read
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "Learn FastAPI"

        # Update
        update_response = client.put(
            f"/todos/{todo_id}",
            json={"status": "in_progress"}
        )
        assert update_response.status_code == 200

        # Read again to verify update
        get_response2 = client.get(f"/todos/{todo_id}")
        assert get_response2.json()["status"] == "in_progress"

        # Delete
        delete_response = client.delete(f"/todos/{todo_id}")
        assert delete_response.status_code == 204

        # Verify deletion
        get_response3 = client.get(f"/todos/{todo_id}")
        assert get_response3.status_code == 404
