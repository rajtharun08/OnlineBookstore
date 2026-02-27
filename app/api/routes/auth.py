from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.dependencies import get_db,role_required,get_current_user
from app.schemas.user_schema import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter()
user_repo = UserRepository()
user_service = UserService(user_repo)

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, user_in)

@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return user_service.login_user(db, email=form_data.username, password=form_data.password)
