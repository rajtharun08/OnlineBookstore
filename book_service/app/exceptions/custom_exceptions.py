class BookServiceException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class BookNotFoundException(BookServiceException):
    def __init__(self, book_id: str):
        super().__init__(f"Book with ID {book_id} does not exist or was deleted.", status_code=404)

class OutOfStockException(BookServiceException):
    def __init__(self, book_id: str):
        super().__init__(f"Book {book_id} is currently out of stock.", status_code=400)