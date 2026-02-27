import re
from app.exceptions.custom_exceptions import OnlineBookstoreException

def validate_email_format(email: str):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(regex, email):
        raise OnlineBookstoreException(message="Invalid email format", status_code=400)