def test_get_books_public(client):
    response = client.get("/books/")
    assert response.status_code == 200

def test_unauthorized_book_delete(client):
    # Testing that a request without a token fails
    response = client.delete("/books/db0816dd-04c2-408a-a40a-917e3f6381d2")
    assert response.status_code == 401