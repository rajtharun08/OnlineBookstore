from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user_schema import UserResponse
from app.core.dependencies import get_current_user, role_required,get_db
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(["admin"]))
):
    return db.query(User).all()