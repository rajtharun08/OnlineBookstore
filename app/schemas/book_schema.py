from pydantic import BaseModel,Field
from typing import Optional
from uuid import UUID

class BookBase(BaseModel):
    title:str =Field(...,min_length=1,max_length=255)
    author:str= Field(...,min_length=1,max_length=255)
    description:Optional[str]=None
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(default=0, ge=0)

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id:UUID
    class Config:
        from_attributes=True
        
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

