# API Usage Examples

This document provides practical examples for using the TODO API.

## Using cURL

### Create a TODO

```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial",
    "priority": 4
  }'
```

### Get All TODOs

```bash
curl -X GET "http://localhost:8000/todos"
```

### Get TODOs by Status

```bash
curl -X GET "http://localhost:8000/todos?status=in_progress"
```

### Get TODOs by Priority

```bash
curl -X GET "http://localhost:8000/todos?priority=5"
```

### Get a Single TODO

```bash
curl -X GET "http://localhost:8000/todos/todo-abc123"
```

### Update a TODO

```bash
curl -X PUT "http://localhost:8000/todos/todo-abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "priority": 5
  }'
```

### Delete a TODO

```bash
curl -X DELETE "http://localhost:8000/todos/todo-abc123"
```

### Get Statistics

```bash
curl -X GET "http://localhost:8000/todos/stats/summary"
```

## Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a TODO
todo_data = {
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "priority": 5,
    "status": "in_progress"
}
response = requests.post(f"{BASE_URL}/todos", json=todo_data)
new_todo = response.json()
print(f"Created TODO: {new_todo['id']}")

# Get all TODOs
response = requests.get(f"{BASE_URL}/todos")
todos = response.json()
print(f"Total TODOs: {len(todos)}")

# Update TODO
todo_id = new_todo['id']
update_data = {"status": "completed"}
response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
updated_todo = response.json()
print(f"Updated status: {updated_todo['status']}")

# Get statistics
response = requests.get(f"{BASE_URL}/todos/stats/summary")
stats = response.json()
print(f"Statistics: {stats}")

# Delete TODO
response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
print(f"Deleted: {response.status_code == 204}")
```

## Using JavaScript/Fetch

```javascript
const BASE_URL = 'http://localhost:8000';

// Create a TODO
async function createTodo() {
  const response = await fetch(`${BASE_URL}/todos`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title: 'Build frontend',
      description: 'Create React frontend for TODO app',
      priority: 4
    })
  });

  const todo = await response.json();
  console.log('Created:', todo);
  return todo;
}

// Get all TODOs
async function getAllTodos() {
  const response = await fetch(`${BASE_URL}/todos`);
  const todos = await response.json();
  console.log('All TODOs:', todos);
  return todos;
}

// Filter by status
async function getInProgressTodos() {
  const response = await fetch(`${BASE_URL}/todos?status=in_progress`);
  const todos = await response.json();
  console.log('In Progress:', todos);
  return todos;
}

// Update TODO
async function updateTodo(todoId) {
  const response = await fetch(`${BASE_URL}/todos/${todoId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      status: 'completed'
    })
  });

  const updated = await response.json();
  console.log('Updated:', updated);
  return updated;
}

// Delete TODO
async function deleteTodo(todoId) {
  const response = await fetch(`${BASE_URL}/todos/${todoId}`, {
    method: 'DELETE'
  });

  console.log('Deleted:', response.status === 204);
  return response.status === 204;
}

// Get statistics
async function getStats() {
  const response = await fetch(`${BASE_URL}/todos/stats/summary`);
  const stats = await response.json();
  console.log('Statistics:', stats);
  return stats;
}

// Usage
(async () => {
  const todo = await createTodo();
  await getAllTodos();
  await updateTodo(todo.id);
  await getStats();
  await deleteTodo(todo.id);
})();
```

## Using HTTPie

```bash
# Create TODO
http POST localhost:8000/todos \
  title="Deploy to production" \
  priority:=5

# Get all TODOs
http GET localhost:8000/todos

# Filter by status
http GET localhost:8000/todos status==completed

# Update TODO
http PUT localhost:8000/todos/todo-abc123 \
  status="in_progress"

# Delete TODO
http DELETE localhost:8000/todos/todo-abc123

# Get statistics
http GET localhost:8000/todos/stats/summary
```

## Error Handling Examples

### Validation Error (422)

```bash
# Empty title
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": ""
  }'

# Response:
# {
#   "detail": [
#     {
#       "loc": ["body", "title"],
#       "msg": "ensure this value has at least 1 characters",
#       "type": "value_error.any_str.min_length"
#     }
#   ]
# }
```

### Not Found Error (404)

```bash
curl -X GET "http://localhost:8000/todos/nonexistent-id"

# Response:
# {
#   "detail": "TODO item with id 'nonexistent-id' not found"
# }
```

## Integration Test Script

```python
#!/usr/bin/env python3
"""
Complete integration test demonstrating all API features.
"""
import requests
import time

BASE_URL = "http://localhost:8000"

def run_integration_test():
    print("=== TODO API Integration Test ===\n")

    # 1. Check health
    print("1. Checking API health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.json()['status']}")

    # 2. Create multiple TODOs
    print("\n2. Creating TODOs...")
    todos = []
    todo_data = [
        {"title": "Setup project", "priority": 5, "status": "completed"},
        {"title": "Write documentation", "priority": 4, "status": "in_progress"},
        {"title": "Add tests", "priority": 4, "status": "in_progress"},
        {"title": "Deploy to production", "priority": 5, "status": "pending"},
    ]

    for data in todo_data:
        response = requests.post(f"{BASE_URL}/todos", json=data)
        todo = response.json()
        todos.append(todo)
        print(f"   Created: {todo['title']} (ID: {todo['id']})")

    # 3. Get all TODOs
    print("\n3. Fetching all TODOs...")
    response = requests.get(f"{BASE_URL}/todos")
    all_todos = response.json()
    print(f"   Total: {len(all_todos)}")

    # 4. Filter by status
    print("\n4. Filtering by status (in_progress)...")
    response = requests.get(f"{BASE_URL}/todos?status=in_progress")
    filtered = response.json()
    print(f"   In Progress: {len(filtered)}")

    # 5. Update a TODO
    print("\n5. Updating TODO status...")
    todo_to_update = todos[1]['id']
    response = requests.put(
        f"{BASE_URL}/todos/{todo_to_update}",
        json={"status": "completed"}
    )
    updated = response.json()
    print(f"   Updated '{updated['title']}' to {updated['status']}")

    # 6. Get statistics
    print("\n6. Getting statistics...")
    response = requests.get(f"{BASE_URL}/todos/stats/summary")
    stats = response.json()
    print(f"   Total: {stats['total']}")
    print(f"   By Status: {stats['by_status']}")
    print(f"   By Priority: {stats['by_priority']}")

    # 7. Delete a TODO
    print("\n7. Deleting a TODO...")
    todo_to_delete = todos[0]['id']
    response = requests.delete(f"{BASE_URL}/todos/{todo_to_delete}")
    print(f"   Deleted: {response.status_code == 204}")

    # 8. Verify deletion
    print("\n8. Verifying deletion...")
    response = requests.get(f"{BASE_URL}/todos/{todo_to_delete}")
    print(f"   Not Found: {response.status_code == 404}")

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    run_integration_test()
```

Save this as `test_integration.py` and run with:

```bash
python test_integration.py
```
