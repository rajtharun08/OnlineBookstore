import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Online Bookstore API"
    
    @property
    def DATABASE_URL(self) -> str:
        return os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback_secret_for_dev_only")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    class Config:
        env_file = ".env"

settings = Settings()