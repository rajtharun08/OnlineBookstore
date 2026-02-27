import pytest
from uuid import uuid4

def test_get_own_profile(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["role"] == "customer"

def test_admin_can_list_all_users(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_customer_cannot_list_all_users(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 403 
    error_msg = response.json().get("message", "").lower()
    assert "permissions" in error_msg

def test_get_user_by_invalid_id(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    random_id = str(uuid4())
    response = client.get(f"/users/{random_id}", headers=headers)
    assert response.status_code == 404
    data = response.json()
    error_text = data.get("message") or data.get("detail") or ""
    assert "not found" in error_text.lower()