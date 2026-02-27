def test_place_order_success(client, user_token, admin_token, db):
    # 1. Create a book as admin
    headers_adm = {"Authorization": f"Bearer {admin_token}"}
    book = client.post("/books/", json={"title": "Test", "author": "A", "price": 10, "stock_quantity": 5}, headers=headers_adm).json()
    
    # 2. Place order as user
    headers_usr = {"Authorization": f"Bearer {user_token}"}
    order_payload = {"items": [{"book_id": book["id"], "quantity": 2}]}
    response = client.post("/orders/", json=order_payload, headers=headers_usr)
    
    assert response.status_code == 201
    assert response.json()["total_price"] == 20.0

def test_insufficient_stock(client, user_token, admin_token):
    headers_adm = {"Authorization": f"Bearer {admin_token}"}
    book = client.post("/books/", json={"title": "Test", "author": "A", "price": 10, "stock_quantity": 1}, headers=headers_adm).json()
    
    headers_usr = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/orders/", json={"items": [{"book_id": book["id"], "quantity": 5}]}, headers=headers_usr)
    assert response.status_code == 400
    assert "stock" in response.json()["message"]

def test_order_history_empty(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/orders/my-orders", headers=headers)
    assert response.status_code == 404

def test_stock_decreases_after_order(client, user_token, admin_token):
    headers_adm = {"Authorization": f"Bearer {admin_token}"}
    book_id = client.post("/books/", json={"title": "StockTest", "author": "A", "price": 10, "stock_quantity": 10}, headers=headers_adm).json()["id"]
    
    headers_usr = {"Authorization": f"Bearer {user_token}"}
    client.post("/orders/", json={"items": [{"book_id": book_id, "quantity": 3}]}, headers=headers_usr)

    book_after = client.get(f"/books/{book_id}").json()
    assert book_after["stock_quantity"] == 7

def test_order_non_existent_book(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/orders/", json={"items": [{"book_id": "00000000-0000-0000-0000-000000000000", "quantity": 1}]}, headers=headers)
    assert response.status_code in [404,400]