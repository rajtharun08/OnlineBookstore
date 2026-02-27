from pydantic import BaseModel
from typing import List, Generic, TypeVar

T = TypeVar("T") # placeholder for any type of item 

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        from_attributes = True