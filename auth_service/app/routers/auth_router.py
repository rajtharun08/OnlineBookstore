from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.session import get_db
from app.schemas.auth_schema import UserCreate, UserResponse, Token
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

user_repo = UserRepository()
auth_service = AuthService(user_repo=user_repo)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = auth_service.user_repo.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
    return auth_service.register(db, user_in)

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = auth_service.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.generate_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def read_users_me(
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user)
):
    repo = UserRepository(db)
    service = AuthService(repo)
    return service.get_current_user_profile(db, current_user_id)