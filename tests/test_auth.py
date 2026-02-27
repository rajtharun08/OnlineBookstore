def test_register_success(client):
    payload = {"email": "new@test.com", "password": "Password123!", "full_name": "Tharun"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == "new@test.com"

def test_register_duplicate_email(client):
    payload = {"email": "dup@test.com", "password": "Password123!", "full_name": "Tharun"}
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["message"]

def test_invalid_email_format(client):
    payload = {"email": "not-an-email", "password": "Password123!", "full_name": "Tharun"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 422

def test_weak_password(client):
    payload = {"email": "weak@test.com", "password": "123", "full_name": "Tharun"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert "at least 8 characters" in response.json()["message"]

def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "t@t.com", "password": "Password123!", "full_name": "T"})
    response = client.post("/auth/login", data={"username": "t@t.com", "password": "wrongpassword"})
    assert response.status_code == 401