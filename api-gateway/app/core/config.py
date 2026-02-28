from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    BOOK_SERVICE_URL: str = "http://localhost:8002"
    ORDER_SERVICE_URL: str = "http://localhost:8003"
    INTERNAL_SERVICE_SECRET: str = "my_internal_communication_secret_123"
    SECRET_KEY: str = "your_super_secret_key"  
    ALGORITHM: str = "HS256"

settings = Settings()