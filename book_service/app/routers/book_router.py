from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse
from app.services.book_service import BookService
from app.repositories.book_repository import BookRepository
from app.core.dependencies import role_required

router = APIRouter(prefix="/books", tags=["Books"])
book_service = BookService(book_repo=BookRepository())


@router.get("/", response_model=List[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    return book_service.list_books(db)


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, 
             dependencies=[Depends(role_required("admin"))])
def create_new_book(book_in: BookCreate, db: Session = Depends(get_db)):
    return book_service.add_book(db, book_in)

@router.put("/{book_id}", response_model=BookResponse, 
            dependencies=[Depends(role_required("admin"))])
def update_existing_book(book_id: str, book_update: BookUpdate, db: Session = Depends(get_db)):
    updated_book = book_service.update_book(db, book_id, book_update)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, 
               dependencies=[Depends(role_required("admin"))])
def delete_book(book_id: str, db: Session = Depends(get_db)):
    success = book_service.remove_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None