import httpx
from app.exceptions.custom_exceptions import InventoryConflictException,ServiceUnavailableException,InventoryUpdateException
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.order_repository import OrderRepository
from app.core.config import settings

class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def place_order(self, db: Session, user_id: str, order_in, token: str):
        async with httpx.AsyncClient() as client:
            #get details from book service
            try:
                book_res = await client.get(
                    f"{settings.BOOK_SERVICE_URL}/books/{order_in.book_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
            except httpx.RequestError:
                raise ServiceUnavailableException("Book Service")

            if book_res.status_code == 404:
                raise InventoryConflictException("The book does not exist in our catalog.")

            book_data = book_res.json()

            # check stock
            if book_data["stock"] < order_in.quantity:
                raise InventoryConflictException(f"Insufficient stock. Available: {book_data['stock']}")

            # Reduce stock in book service
            new_stock = book_data["stock"] - order_in.quantity
        
            update_res = await client.put(
                f"{settings.BOOK_SERVICE_URL}/books/{order_in.book_id}",
                json={"stock": new_stock},
                headers={
                    "Authorization": f"Bearer {token}",
                    "X-Internal-Secret": settings.INTERNAL_SERVICE_SECRET
                }
            )

            if update_res.status_code != 200:
                raise InventoryUpdateException()

            
            order_data = {
                "user_id": user_id,
                "book_id": str(order_in.book_id),
                "quantity": order_in.quantity,
                "total_price": book_data["price"] * order_in.quantity,
                "status": "completed"
            }
            return self.order_repo.create(db, order_data)        
    def get_user_history(self, db: Session, user_id: str):
        return self.order_repo.get_user_orders(db, user_id)

    def get_admin_report(self, db: Session):
        total_orders, total_revenue = self.order_repo.get_sales_summary(db)
        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue
        }