def test_order_reduces_stock(client, db):
    # 1. Login to get a token
    login_res = client.post("/auth/login", data={
        "username": "testuser@example.com", 
        "password": "securepassword123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # 2. Get a book and check initial stock
    book_response = client.get("/books/", headers=headers)
    assert book_response.status_code == 200
    
    book_data = book_response.json()[0]
    book_id = book_data["id"]  
    initial_stock = book_data["stock_quantity"] 

    # 3. Place an order
    order_data = {"items": [{"book_id": book_id, "quantity": 1}]}
    order_response = client.post("/orders/", json=order_data, headers=headers)
    assert order_response.status_code == 201

    # 4. Check stock again and verify deduction
    updated_book_res = client.get(f"/books/{book_id}", headers=headers)
    updated_book = updated_book_res.json()
    
    # Assert that the stock is exactly 1 less than before
    assert updated_book["stock_quantity"] == initial_stock - 1