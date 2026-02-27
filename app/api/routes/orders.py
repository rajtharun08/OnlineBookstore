from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db
from app.core.dependencies import get_current_user
from app.schemas.order_schema import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository
from app.repositories.book_repository import BookRepository

router = APIRouter(prefix="/orders", tags=["Orders"])

order_service = OrderService(
    order_repo=OrderRepository(), 
    book_repo=BookRepository()
)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_new_order(
    order_in: OrderCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # Requirement: Auth
):
    return order_service.place_order(db, user_id=current_user.id, order_in=order_in)

@router.get("/me", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) 
):
    return order_service.get_user_history(db, user_id=current_user.id)