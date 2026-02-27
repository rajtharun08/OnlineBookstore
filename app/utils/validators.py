import re
from app.exceptions.custom_exceptions import OnlineBookstoreException

def validate_email_format(email: str):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(regex, email):
        raise OnlineBookstoreException(message="Invalid email format", status_code=400)

def validate_password_strength(password: str):
    if len(password) < 8:
        raise OnlineBookstoreException(message="Password must be at least 8 characters long", status_code=400)
    if not any(char.isdigit() for char in password):
        raise OnlineBookstoreException(message="Password must contain at least one number", status_code=400)
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise OnlineBookstoreException(message="Password must contain at least one special character", status_code=400)