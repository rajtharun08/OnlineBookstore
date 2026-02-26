from fastapi import FastAPI
from app.api.routes import books
from app.models.base import Base
from app.core.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Bookstore API",
    description="A professional API for managing book inventory",
    version="1.0.0"
)

app.include_router(books.router, prefix="/books", tags=["Books"])

@app.get("/")
def root():
    return {"message": "Welcome to the Online Bookstore API! Visit /docs for the Swagger UI."}
from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.book_repository import BookRepository
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.dependencies import get_db
from app.schemas.book_schema import BookResponse, BookCreate
from app.services.book_service import BookService

router=APIRouter(prefix="/books")
book_repo=BookRepository()
book_service=BookService(book_repo=book_repo)

@router.post("/",response_model=BookResponse,status_code=status.HTTP_201_CREATED)
def create_book(book:BookCreate,db:Session=Depends(get_db)):
    return book_service.create_book(db,book)

@router.get("/",response_model=List[BookResponse],status_code=status.HTTP_200_OK)
def get_all_books(db:Session=Depends(get_db)):
    return book_service.get_all_books(db)

@router.get("/{book_id}", response_model=BookResponse)
def read_book(book_id: UUID, db: Session = Depends(get_db)):
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
