from uuid import UUID
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate

class UserRepository:
    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, user_id: UUID):
        return db.query(User).filter(User.id == user_id).first()
    
    def create(self, db: Session, user_in: UserCreate, hashed_pw: str):
        db_user = User(
            email=user_in.email,
            password_hash=hashed_pw, 
            role=user_in.role 
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user