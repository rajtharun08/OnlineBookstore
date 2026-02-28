from fastapi import APIRouter, Depends
from app.schemas.order_schema import OrderCreate
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository
from app.core.security import get_current_user, role_required

router = APIRouter(prefix="/orders", tags=["Orders"])

# Wire them up: Repo -> Service
order_service = OrderService(order_repo=OrderRepository())

@router.post("/")
async def checkout(order_in : OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return await order_service.place_order(db, user["id"], order_in, user["token"])

@router.get("/my-orders")
def my_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return order_service.get_user_history(db, user["id"])

@router.get("/admin/sales-report")
def sales_report(
    db: Session = Depends(get_db), 
    admin=Depends(role_required("admin"))
):
    return order_service.get_admin_report(db)