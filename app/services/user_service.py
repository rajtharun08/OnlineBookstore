from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password
from app.exceptions.custom_exceptions import OnlineBookstoreException
from app.core.security import verify_password, create_access_token

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, db: Session, user_in: UserCreate):
        if self.user_repo.get_by_email(db, user_in.email):
            raise OnlineBookstoreException(message="Email already registered", status_code=400)
        
        hashed_pw = hash_password(user_in.password)
        return self.user_repo.create(db, user_in, hashed_pw)
    
    def authenticate_user(self, db: Session, email: str, password: str):
        user = self.user_repo.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            return False
        return user