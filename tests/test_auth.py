def test_register_user(client):
    response = client.post("/auth/register", json={
        "email": "testuser@example.com",
        "password": "securepassword123",
        "full_name": "Test User"
    })
    # If user already exists, we expect 400, otherwise 201
    assert response.status_code in [201, 400]

def test_login_success(client):
    response = client.post("/auth/login", data={
        "username": "testuser@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()