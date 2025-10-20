# TODO API Backend

A production-ready FastAPI backend for managing TODO items with full CRUD operations, comprehensive validation, and RESTful API design.

## Features

- **Full CRUD Operations**: Create, Read, Update, and Delete TODO items
- **Data Validation**: Robust validation using Pydantic models
- **Status Management**: Track TODOs with pending, in_progress, and completed states
- **Priority System**: Assign priorities from 1-5 (5 being highest)
- **Filtering**: Filter TODOs by status and priority
- **Statistics**: Get insights into your TODO distribution
- **API Documentation**: Auto-generated interactive docs with Swagger UI
- **CORS Support**: Ready for frontend integration
- **Comprehensive Tests**: Full test coverage with pytest

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Python 3.8+**: Required Python version
- **pytest**: Testing framework
- **uvicorn**: ASGI server

## Project Structure

```
/workspace/
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic data models
├── database.py          # In-memory database (replace with DB in production)
├── test_main.py         # Comprehensive test suite
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Production Deployment

For production, use a production-grade ASGI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Root & Health

- `GET /` - API information
- `GET /health` - Health check endpoint

### TODO Operations

#### Create a TODO
```http
POST /todos
Content-Type: application/json

{
  "title": "Complete FastAPI backend",
  "description": "Implement CRUD operations",
  "status": "in_progress",
  "priority": 4
}
```

**Response**: `201 Created`
```json
{
  "id": "todo-abc123",
  "title": "Complete FastAPI backend",
  "description": "Implement CRUD operations",
  "status": "in_progress",
  "priority": 4,
  "created_at": "2025-10-20T12:00:00",
  "updated_at": "2025-10-20T12:00:00"
}
```

#### Get All TODOs
```http
GET /todos
```

Optional query parameters:
- `status`: Filter by status (pending, in_progress, completed)
- `priority`: Filter by priority (1-5)

**Example**: `GET /todos?status=in_progress&priority=5`

#### Get Single TODO
```http
GET /todos/{todo_id}
```

**Response**: `200 OK` or `404 Not Found`

#### Update TODO
```http
PUT /todos/{todo_id}
Content-Type: application/json

{
  "title": "Updated title",
  "status": "completed"
}
```

All fields are optional. Only provided fields will be updated.

**Response**: `200 OK` or `404 Not Found`

#### Delete TODO
```http
DELETE /todos/{todo_id}
```

**Response**: `204 No Content` or `404 Not Found`

### Statistics

#### Get TODO Statistics
```http
GET /todos/stats/summary
```

**Response**:
```json
{
  "total": 10,
  "by_status": {
    "pending": 3,
    "in_progress": 5,
    "completed": 2
  },
  "by_priority": {
    "1": 2,
    "2": 3,
    "3": 2,
    "4": 1,
    "5": 2
  }
}
```

## Data Models

### TodoCreate
```python
{
  "title": str,              # Required, 1-200 characters
  "description": str,        # Optional, max 1000 characters
  "status": str,            # Optional, default: "pending"
  "priority": int           # Optional, default: 1, range: 1-5
}
```

### TodoUpdate
```python
{
  "title": str,              # Optional, 1-200 characters
  "description": str,        # Optional, max 1000 characters
  "status": str,            # Optional
  "priority": int           # Optional, range: 1-5
}
```

### TodoResponse
```python
{
  "id": str,                 # Unique identifier
  "title": str,
  "description": str,
  "status": str,            # "pending" | "in_progress" | "completed"
  "priority": int,          # 1-5
  "created_at": datetime,
  "updated_at": datetime
}
```

## Running Tests

Execute the test suite:

```bash
pytest test_main.py -v
```

Run with coverage:

```bash
pytest test_main.py -v --cov=. --cov-report=html
```

### Test Coverage

The test suite includes:
- Root and health endpoint tests
- CRUD operation tests
- Validation tests
- Error handling tests
- Filtering tests
- Statistics tests
- Integration workflow tests

## Development Guidelines

### Adding New Features

1. **Update Models**: Add/modify Pydantic models in `models.py`
2. **Update Database**: Modify database operations in `database.py`
3. **Add Endpoints**: Create new endpoints in `main.py`
4. **Write Tests**: Add comprehensive tests in `test_main.py`
5. **Update Documentation**: Keep this README up to date

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Add docstrings to all classes and functions
- Keep functions focused and single-purpose

## Production Considerations

### Database Migration

The current implementation uses an in-memory database. For production:

1. **Choose a Database**: PostgreSQL, MySQL, MongoDB, etc.
2. **Add ORM**: Use SQLAlchemy or similar
3. **Add Migrations**: Use Alembic for schema migrations
4. **Update `database.py`**: Replace in-memory storage

Example with SQLAlchemy:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### Security

1. **Add Authentication**: Implement JWT or OAuth2
2. **Rate Limiting**: Protect against abuse
3. **Input Sanitization**: Already handled by Pydantic
4. **HTTPS**: Use SSL/TLS in production
5. **Environment Variables**: Store sensitive config in env vars

### Monitoring

1. **Logging**: Add structured logging
2. **Metrics**: Integrate Prometheus or similar
3. **Error Tracking**: Use Sentry or similar
4. **Health Checks**: Already implemented at `/health`

### CORS Configuration

Update CORS settings in `main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify exact origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## API Response Codes

- `200 OK`: Successful GET/PUT request
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Integration with Frontend

This backend is designed to work with frontend applications. Example fetch request:

```javascript
// Create a TODO
const response = await fetch('http://localhost:8000/todos', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'New TODO',
    priority: 3
  })
});

const todo = await response.json();
console.log(todo);
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:
```bash
uvicorn main:app --port 8001
```

### Import Errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Test Failures

Clear any cached data and run tests:
```bash
pytest test_main.py -v --cache-clear
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.

## Roadmap

Future enhancements:
- [ ] Add user authentication
- [ ] Implement database persistence
- [ ] Add due dates and reminders
- [ ] Support for TODO categories/tags
- [ ] File attachments
- [ ] Real-time updates with WebSockets
- [ ] GraphQL API support
- [ ] Mobile app integration

## Contact

Built with the MEU Framework for agent-driven development.
