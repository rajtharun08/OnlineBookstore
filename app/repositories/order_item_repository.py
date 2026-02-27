from sqlalchemy.orm import Session
from app.models.order_item import OrderItem

class OrderItemRepository:
    def create_items(self, db: Session, items: list[OrderItem]):
        db.add_all(items)
        db.flush() 
        return items