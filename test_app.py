import sys
sys.path.insert(0, '.')

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_hello_endpoint():
    """Test the /hello endpoint returns the expected format."""
    response = client.get("/hello")
    assert response.status_code == 200

    # Use response.json() for the assertion as requested (handle string response)
    response_data = response.json()

    # The FastAPI endpoint returns a string, so response.json() gives us the string directly
    assert isinstance(response_data, str)
    assert response_data.startswith("Hello, World! - Test ")

    # Verify timestamp format is present (basic check)
    assert "T" in response_data  # ISO format contains 'T'

    print(f"Test passed! Response: {response_data}")
