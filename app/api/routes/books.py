from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.dependencies import get_db
from app.schemas.book_schema import BookResponse, BookCreate
from app.services.book_service import BookService
from app.repositories.book_repository import BookRepository
from app.schemas.book_schema import BookResponse, BookUpdate
from app.core.dependencies import get_current_user

from app.core.dependencies import role_required
router = APIRouter(prefix="/books")
book_repo = BookRepository()
book_service = BookService(book_repo=book_repo)

@router.post("/", response_model=BookResponse)
def create_book(book_in: BookCreate, db: Session = Depends(get_db),current_user = Depends(role_required(["admin"]))):
    return book_service.create_book(db, book_in)

@router.get("/", response_model=List[BookResponse])
def read_books(db: Session = Depends(get_db),skip:int=0,limit:int=10,current_user = Depends(role_required(["customer", "admin"]))):
    return book_service.get_all_books(db,skip=skip,limit=limit)

@router.get("/{book_id}", response_model=BookResponse)
def read_book(book_id: UUID, db: Session = Depends(get_db)):
    return book_service.get_book_by_id(db, book_id)


@router.put("/{id}", response_model=BookResponse)
def update_existing_book(id: UUID, book_in: BookUpdate, db: Session = Depends(get_db),current_user = Depends(get_current_user) ):
    return book_service.update_book(db, book_id=id, book_in=book_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_book(id: UUID, db: Session = Depends(get_db),current_user = Depends(get_current_user) ):
    book_service.delete_book(db, book_id=id)
    return None