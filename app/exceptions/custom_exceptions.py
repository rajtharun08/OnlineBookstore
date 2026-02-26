from fastapi import status
class OnlineBookstoreException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code

class BookNotFoundException(OnlineBookstoreException):
    def __init__(self, book_id: str):
        super().__init__(
            message=f"Book with ID '{book_id}' does not exist.",
            status_code=status.HTTP_404_NOT_FOUND
        )

class DatabaseConnectionException(OnlineBookstoreException):
    def __init__(self):
        super().__init__(
            message="Could not connect to the database.",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )