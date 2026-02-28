import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_super_secret_key")
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:Tharun%4008@localhost:5432/book_db")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()