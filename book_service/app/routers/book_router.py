from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse
from app.services.book_service import BookService
from app.repositories.book_repository import BookRepository
from app.core.dependencies import get_current_user, role_required
from app.core.config import settings

router = APIRouter(prefix="/books", tags=["Books"])
book_service = BookService(book_repo=BookRepository())


@router.get("/", response_model=List[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    return book_service.list_books(db)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: str, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, 
             dependencies=[Depends(role_required("admin"))])
def create_new_book(book_in: BookCreate, db: Session = Depends(get_db)):
    return book_service.add_book(db, book_in)

@router.put("/{book_id}")
def update_book(
    book_id: str, 
    book_update: BookUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    x_internal_secret: str = Header(None) 
):
    if current_user["role"] == "admin":
        return book_service.update_book(db, book_id, book_update)

    if x_internal_secret == settings.INTERNAL_SERVICE_SECRET: # Validate internal secret for service-to-service calls
        update_data = book_update.model_dump(exclude_unset=True)
        if any(key in update_data for key in ["price", "title", "author"]):
             raise HTTPException(status_code=403, detail="Internal service can only update stock")
        return book_service.update_book(db, book_id, book_update)

    raise HTTPException(status_code=403, detail="Not authorized to update catalog")

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, 
               dependencies=[Depends(role_required("admin"))])
def delete_book(book_id: str, db: Session = Depends(get_db)):
    success = book_service.remove_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None