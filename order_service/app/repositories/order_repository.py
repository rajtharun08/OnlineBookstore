from sqlalchemy import func

from sqlalchemy.orm import Session
from app.models.order import Order

class OrderRepository:
    def create(self, db: Session, order_data: dict):
        db_order = Order(**order_data)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    
    def get_user_orders(self, db: Session, user_id: str):
        return db.query(Order).filter(Order.user_id == user_id).all()
    
    def get_all_orders(self, db: Session):
        return db.query(Order).all()
    
    def get_sales_summary(self, db: Session):
        total_orders = db.query(Order).count()
        total_revenue = db.query(func.sum(Order.total_price)).scalar() or 0
        return total_orders, total_revenue