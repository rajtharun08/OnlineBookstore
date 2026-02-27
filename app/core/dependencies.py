from app.core.database import SessionLocal
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, jwt, JWTError
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.config import settings
from app.exceptions.custom_exceptions import OnlineBookstoreException, UnauthorizedRoleException
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise OnlineBookstoreException(message="Invalid token payload", status_code=401)
            
    except ExpiredSignatureError:
        raise OnlineBookstoreException(message="Token has expired", status_code=401)
    except JWTError:
        raise OnlineBookstoreException(message="Could not validate credentials", status_code=401)
    user_repo = UserRepository()
    user = user_repo.get_by_id(db, UUID(user_id))
    
    if user is None:
        raise OnlineBookstoreException(message="User not found", status_code=401)
        
    return user

def role_required(allowed_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise UnauthorizedRoleException()
        return current_user
    return role_checker