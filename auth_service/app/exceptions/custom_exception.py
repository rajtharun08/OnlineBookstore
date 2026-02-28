class AuthServiceException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class UserAlreadyExistsException(AuthServiceException):
    def __init__(self, email: str):
        super().__init__(f"Account with email {email} already exists.", 400)

class InvalidCredentialsException(AuthServiceException):
    def __init__(self):
        super().__init__("Invalid email or password.", 401)

class UnauthorizedException(AuthServiceException):
    def __init__(self):
        super().__init__("You are not authorized to perform this action.", 403)