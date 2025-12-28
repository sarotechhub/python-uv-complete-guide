import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_root(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]


def test_list_items_empty(client):
    """Test listing items when empty."""
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json()["items"] == []


def test_create_item(client):
    """Test creating an item."""
    item_data = {
        "id": 1,
        "name": "Test Item",
        "description": "A test item",
        "price": 9.99,
        "in_stock": True
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json()["created"]["name"] == "Test Item"


def test_get_item(client):
    """Test getting a specific item."""
    # Create an item first
    item_data = {
        "id": 1,
        "name": "Test Item",
        "price": 9.99
    }
    client.post("/items/", json=item_data)
    
    # Get the item
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"


def test_get_nonexistent_item(client):
    """Test getting a non-existent item."""
    response = client.get("/items/999")
    assert response.status_code == 404
