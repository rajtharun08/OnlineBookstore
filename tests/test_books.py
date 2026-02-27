def test_get_books_empty(client):
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json()["items"] == []

def test_create_book_as_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {"title": "FastAPI Guide", "author": "Tharun", "price": 29.99, "stock_quantity": 10}
    response = client.post("/books/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "FastAPI Guide"

def test_create_book_unauthorized(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/books/", json={"title": "Hack"}, headers=headers)
    assert response.status_code == 403

def test_pagination_limit(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    for i in range(5):
        client.post("/books/", json={"title": f"B{i}", "author": "A", "price": 10, "stock_quantity": 1}, headers=headers)
    response = client.get("/books/?size=2")
    assert len(response.json()["items"]) == 2

def test_update_book_not_found(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.put("/books/00000000-0000-0000-0000-000000000000", json={"price": 5}, headers=headers)
    assert response.status_code == 404