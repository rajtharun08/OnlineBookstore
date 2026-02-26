import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Online Bookstore API"
    
    @property
    def DATABASE_URL(self) -> str:
        return os.getenv("DATABASE_URL")

settings = Settings()