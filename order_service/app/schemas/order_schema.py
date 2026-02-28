from pydantic import BaseModel
from uuid import UUID
from typing import List

class OrderCreate(BaseModel):
    book_id: UUID
    quantity: int

class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    book_id: UUID
    quantity: int
    total_price: float
    status: str

    class Config:
        from_attributes = True