from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository
from app.repositories.book_repository import BookRepository
from app.schemas.order_schema import OrderCreate
from app.exceptions.custom_exceptions import OnlineBookstoreException
from uuid import UUID

class OrderService:
    def __init__(self, order_repo: OrderRepository, book_repo: BookRepository):
        self.order_repo = order_repo
        self.book_repo = book_repo

    def place_order(self, db: Session, user_id: UUID, order_in: OrderCreate):
        total_price = 0
        items_to_create = []

        # 1. Validate books and calculate total
        for item in order_in.items:
            book = self.book_repo.get_by_id(db, item.book_id)
            if not book:
                raise OnlineBookstoreException(message=f"Book {item.book_id} not found", status_code=404)
            
            total_price += book.price * item.quantity
            items_to_create.append((book, item.quantity))

        # 2. Create the Order
        db_order = self.order_repo.create_order(db, user_id, total_price)

        # 3. Create Order Items
        for book, quantity in items_to_create:
            self.order_repo.create_order_item(
                db, 
                order_id=db_order.id, 
                book_id=book.id, 
                quantity=quantity, 
                price=book.price
            )

        db.commit()
        db.refresh(db_order)
        return db_order