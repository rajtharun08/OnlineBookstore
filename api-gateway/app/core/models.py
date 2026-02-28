from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str
    
# --- AUTH VALIDATION ---
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Must be a valid email address")
    password: str = Field(..., min_length=4, description="Password must be at least 4 characters")
    role: Optional[str] = Field("customer", pattern="^(admin|customer)$")

# --- BOOK VALIDATION ---
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=2)
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    stock: int = Field(..., ge=0, description="Stock cannot be negative")

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=2)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

# --- ORDER VALIDATION ---
class OrderCreate(BaseModel):
    book_id: UUID = Field(..., description="Must be a valid UUID of a book")
    quantity: int = Field(..., gt=0, description="Must order at least 1 book")