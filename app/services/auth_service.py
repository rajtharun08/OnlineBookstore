from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.exceptions.custom_exceptions import OnlineBookstoreException

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def login_user(self, db: Session, email: str, password: str):
        user = self.user_repo.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise OnlineBookstoreException(message="Invalid email or password", status_code=401)
        
        access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}