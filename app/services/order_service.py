from sqlalchemy.orm import Session
from uuid import UUID
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.book_repository import BookRepository
from app.schemas.order_schema import OrderCreate
from app.models.order_item import OrderItem
from app.exceptions.custom_exceptions import InsufficientStockException, OnlineBookstoreException

class OrderService:
    def __init__(
        self, 
        order_repo: OrderRepository, 
        book_repo: BookRepository, 
        item_repo: OrderItemRepository # Injecting the item repo here
    ):
        self.order_repo = order_repo
        self.book_repo = book_repo
        self.item_repo = item_repo

    def place_order(self, db: Session, user_id: UUID, order_in: OrderCreate):
        total_price = 0
        validated_items = []

        # 1. Validate stock and calculate price snapshot
        for item in order_in.items:
            book = self.book_repo.get_by_id(db, item.book_id)
            if not book or book.stock_quantity < item.quantity:
              raise InsufficientStockException(book_title=book.title if book else "Unknown Book")
            
            # Reduce stock and prepare item data
            book.stock_quantity -= item.quantity
            total_price += book.price * item.quantity
            validated_items.append({"book": book, "qty": item.quantity})

        # 2. Create the Order entry
        new_order = self.order_repo.create_order(db, user_id, total_price)

        # 3. Create OrderItems directly using the Item Repository
        db_items = [
            OrderItem(
                order_id=new_order.id, 
                book_id=i["book"].id, 
                quantity=i["qty"], 
                price_at_purchase=i["book"].price
            ) for i in validated_items
        ]
        self.item_repo.create_items(db, db_items)

        db.commit()
        db.refresh(new_order)
        return new_order
    
    def get_user_history(self, db: Session, user_id: UUID):
        return self.order_repo.get_user_orders(db, user_id)

    def get_admin_report(self, db: Session):
        return self.order_repo.get_sales_stats(db)