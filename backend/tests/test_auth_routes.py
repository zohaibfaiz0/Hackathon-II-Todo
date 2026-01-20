import pytest
from fastapi.testclient import TestClient
from src.hackathon_todo_api.main import app
from src.hackathon_todo_api.routes.auth import authenticate_user, get_password_hash


def test_password_hashing():
    """Test that password hashing works correctly"""
    password = "testpassword123"
    hashed = get_password_hash(password)

    # We can't directly verify the hash, but we can ensure it's different from the original
    assert password != hashed
    assert isinstance(hashed, str)
    assert len(hashed) > 0


def test_auth_route_exists():
    """Test that auth routes are registered"""
    client = TestClient(app)

    # Test that the app contains auth routes (they will return 422 for missing body, not 404)
    response = client.post("/api/auth/register")
    assert response.status_code in [422, 400]  # Unprocessable entity or bad request means route exists

    response = client.post("/api/auth/login")
    assert response.status_code in [422, 400]  # Route exists


if __name__ == "__main__":
    test_password_hashing()
    test_auth_route_exists()
    print("Auth tests passed!")