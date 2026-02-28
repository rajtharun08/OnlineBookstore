from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password

class UserRepository:
    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user_data: dict):
        user_data["password_hash"] = hash_password(user_data.pop("password"))
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user