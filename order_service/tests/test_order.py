import pytest
from app.main import app
from app.routers import order_router

async def mock_json_response(data):
    return data

def test_place_order_success(client, mock_customer_user, mock_book_api):
    app.dependency_overrides[order_router.get_current_user] = lambda: mock_customer_user
    
    mock_book_api["get"].return_value.status_code = 200
    mock_book_api["get"].return_value.json = lambda: mock_json_response({
        "id": "00000000-0000-0000-0000-000000000000", 
        "price": 100.0, 
        "stock": 10
    })
    mock_book_api["put"].return_value.status_code = 200

    response = client.post("/orders/", json={
        "book_id": "00000000-0000-0000-0000-000000000000",
        "quantity": 1
    })
    
    app.dependency_overrides.clear()
    assert response.status_code in [200, 201]

def test_place_order_out_of_stock(client, mock_customer_user, mock_book_api):
    app.dependency_overrides[order_router.get_current_user] = lambda: mock_customer_user
    
    mock_book_api["get"].return_value.status_code = 200
    mock_book_api["get"].return_value.json = lambda: mock_json_response({
        "id": "00000000-0000-0000-0000-000000000000", 
        "price": 100.0, 
        "stock": 0
    })

    response = client.post("/orders/", json={
        "book_id": "00000000-0000-0000-0000-000000000000",
        "quantity": 1
    })
    
    app.dependency_overrides.clear()
    assert response.status_code == 400

def test_place_order_book_not_found(client, mock_customer_user, mock_book_api):
    app.dependency_overrides[order_router.get_current_user] = lambda: mock_customer_user
    mock_book_api["get"].return_value.status_code = 404

    response = client.post("/orders/", json={
        "book_id": "00000000-0000-0000-0000-000000000000",
        "quantity": 1
    })
    
    app.dependency_overrides.clear()
    assert response.status_code == 400

def test_get_my_orders_empty(client, mock_customer_user):
    app.dependency_overrides[order_router.get_current_user] = lambda: mock_customer_user
    response = client.get("/orders/my-orders")
    app.dependency_overrides.clear()
    assert response.status_code == 200

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "online"