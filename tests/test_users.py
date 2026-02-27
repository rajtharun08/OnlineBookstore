import pytest
from uuid import UUID

def test_get_own_profile(client):
    """Verifies that a logged-in user can retrieve their own profile data."""
    # 1. Login to get token
    login_data = {"username": "testuser@example.com", "password": "securepassword123"}
    login_res = client.post("/auth/login", data=login_data)
    token = login_res.json()["access_token"]
    
    # 2. Access profile
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"
    assert "id" in response.json()

def test_user_role_assignment(client, db):
    """Ensures that new users are assigned the 'customer' role by default."""
    from app.models.user import User
    user = db.query(User).filter(User.email == "testuser@example.com").first()
    
    assert user is not None
    assert user.role == "customer" # Default role check

def test_unauthorized_profile_access(client):
    """Verifies that accessing profile without a token returns 401."""
    response = client.get("/users/me")
    assert response.status_code == 401