from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order_schema import OrderCreate
from uuid import UUID

class OrderRepository:
    def create_order(self, db: Session, user_id: UUID, total_price: float):
        db_order = Order(
            user_id=user_id,
            total_price=total_price,
            status="completed"
        )
        db.add(db_order)
        db.flush()  # gets us the order.id 
        return db_order

    def create_order_item(self, db: Session, order_id: UUID, book_id: UUID, quantity: int, price: float):
        db_item = OrderItem(
            order_id=order_id,
            book_id=book_id,
            quantity=quantity,
            price_at_purchase=price
        )
        db.add(db_item)
        return db_item

    def get_user_orders(self, db: Session, user_id: UUID):
        return db.query(Order).filter(Order.user_id == user_id).all()