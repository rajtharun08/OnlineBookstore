from http.client import HTTPException

from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.exceptions.custom_exception import UserAlreadyExistsException, InvalidCredentialsException
class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, db: Session, user_in):
        existing_user = self.user_repo.get_by_email(db, user_in.email)
        if existing_user:
            raise  UserAlreadyExistsException(user_in.email)
        return self.user_repo.create(db, user_in.model_dump())

    def authenticate(self, db: Session, email: str, password: str):
        user = self.user_repo.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsException()
        return user

    def generate_token(self, user):
        return create_access_token(data={
            "sub": str(user.id),
            "role": user.role,
            "email": user.email
        })
    
    from fastapi import HTTPException

def get_current_user_profile(self, db: Session, user_id: int):
    user = self.user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user