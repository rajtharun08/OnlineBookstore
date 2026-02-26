from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.dependencies import get_db
from app.schemas.book_schema import BookResponse, BookCreate
from app.services.book_service import BookService
from app.repositories.book_repository import BookRepository

router = APIRouter(prefix="/books")
book_repo = BookRepository()
book_service = BookService(book_repo=book_repo)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db, book)

@router.get("/", response_model=List[BookResponse])
def read_books(db: Session = Depends(get_db),skip:int=0,limit:int=10):
    return book_service.get_all_books(db,skip=skip,limit=limit)

@router.get("/{book_id}", response_model=BookResponse)
def read_book(book_id: UUID, db: Session = Depends(get_db)):
    return book_service.get_book_by_id(db, book_id)
    