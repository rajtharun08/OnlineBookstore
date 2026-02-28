class OrderServiceException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class OrderNotFoundException(OrderServiceException):
    def __init__(self, order_id: str):
        super().__init__(f"Order {order_id} not found.", 404)

class InventoryConflictException(OrderServiceException):
    def __init__(self, message: str):
        super().__init__(message, 400)

class ServiceUnavailableException(OrderServiceException):
    def __init__(self, service_name: str):
        super().__init__(f"The {service_name} is currently unavailable.", 503)

class InventoryUpdateException(OrderServiceException):
    def __init__(self):
        super().__init__("Failed to synchronize inventory with the Book Service.", status_code=502)