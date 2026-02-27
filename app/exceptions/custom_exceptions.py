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
        
class InsufficientStockException(OnlineBookstoreException):
    def __init__(self, book_title: str):
        super().__init__(
            message=f"Sorry, '{book_title}' is out of stock or has insufficient quantity.",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class UnauthorizedRoleException(OnlineBookstoreException):
    def __init__(self):
        super().__init__(
            message="You do not have the required permissions to perform this action.",
            status_code=status.HTTP_403_FORBIDDEN
        )