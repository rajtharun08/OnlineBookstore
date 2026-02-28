from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    price: float
    stock: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class BookResponse(BookBase):
    id: UUID

    class Config:
        from_attributes = True