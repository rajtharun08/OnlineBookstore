import pytest

def test_register_user_success(client):
    response = client.post("/auth/register", json={
        "email": "tharun@example.com", 
        "password": "strongpassword123"
    })
    assert response.status_code in [200, 201]
    assert response.json()["email"] == "tharun@example.com"

def test_register_duplicate_email(client):
    user_data = {"email": "duplicate@example.com", "password": "password123"}
    client.post("/auth/register", json=user_data)
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already " in response.json()["detail"].lower()

def test_login_success(client):
    client.post("/auth/register", json={
        "email": "login@example.com", 
        "password": "password123"
    })
    
    response = client.post("/auth/login", data={
        "username": "login@example.com", 
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    client.post("/auth/register", json={
        "email": "wrong@example.com", 
        "password": "password123"
    })
    
    response = client.post("/auth/login", data={
        "username": "wrong@example.com", 
        "password": "notthepassword"
    })
    assert response.status_code == 401

def test_invalid_email_format(client):
    response = client.post("/auth/register", json={
        "email": "not-an-email", 
        "password": "password123"
    })
    assert response.status_code == 422