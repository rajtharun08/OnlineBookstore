from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, db: Session, user_in):
        return self.user_repo.create(db, user_in.model_dump())

    def authenticate(self, db: Session, email: str, password: str):
        user = self.user_repo.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    def generate_token(self, user):
        return create_access_token(data={
            "sub": str(user.id),
            "role": user.role,
            "email": user.email
        })