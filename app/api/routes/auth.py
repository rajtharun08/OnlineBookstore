from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter()
user_repo = UserRepository()
user_service = UserService(user_repo)

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a user with a default 'customer' role."""
    return user_service.register_user(db, user_in)

@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """Login using Email and Password to get a JWT Token."""
    return user_service.login_user(db, email=form_data.username, password=form_data.password)