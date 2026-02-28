import pytest
from app.main import app
from app.core.dependencies import get_current_user

def test_create_book_as_admin(client, mock_admin_user):
    app.dependency_overrides[get_current_user] = lambda: mock_admin_user
    response = client.post("/books/", json={
        "title": "Python Microservices",
        "author": "Tharun",
        "price": 599.0,
        "stock": 100
    })
    assert response.status_code in [200, 201]
    assert response.json()["title"] == "Python Microservices"
    app.dependency_overrides.clear()

def test_create_book_unauthorized(client, mock_customer_user):
    app.dependency_overrides[get_current_user] = lambda: mock_customer_user
    response = client.post("/books/", json={
        "title": "Hack the Planet",
        "author": "Anonymous",
        "price": 0.0,
        "stock": 1
    })
    assert response.status_code == 403
    app.dependency_overrides.clear()

def test_get_all_books_pagination(client, mock_admin_user):
    app.dependency_overrides[get_current_user] = lambda: mock_admin_user
    client.post("/books/", json={"title": "Book A", "author": "Auth", "price": 10.0, "stock": 5})
    
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 1
    app.dependency_overrides.clear()

def test_update_book_stock(client, mock_admin_user):
    app.dependency_overrides[get_current_user] = lambda: mock_admin_user
    # Create
    created = client.post("/books/", json={"title": "StockTest", "author": "A", "price": 10.0, "stock": 5}).json()
    
    # Update
    book_id = created["id"]
    response = client.put(f"/books/{book_id}", json={"stock": 50})
    assert response.status_code == 200
    assert response.json()["stock"] == 50
    app.dependency_overrides.clear()

def test_delete_book_not_found(client, mock_admin_user):
    app.dependency_overrides[get_current_user] = lambda: mock_admin_user
    random_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/books/{random_uuid}")
    assert response.status_code == 404
    app.dependency_overrides.clear()