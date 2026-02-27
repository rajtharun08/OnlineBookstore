from pydantic import BaseModel
from uuid import UUID
from typing import List
from datetime import datetime

class OrderItemCreate(BaseModel):
    book_id: UUID
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    book_id: UUID
    quantity: int
    price_at_purchase: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: UUID
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True