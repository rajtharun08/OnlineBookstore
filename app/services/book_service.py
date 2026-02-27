from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID
import math

from app.schemas.book_schema import BookCreate, BookUpdate
from app.repositories.book_repository import BookRepository
from app.exceptions.custom_exceptions import BookNotFoundException, OnlineBookstoreException
from app.models.book import Book

class BookService:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo
    
    def get_all_books(self, db: Session, page: int = 1, size: int = 10):
        skip = (page - 1) * size
        books = self.book_repo.get_all(db, skip=skip, limit=size)
        total_items = db.query(Book).count()
        total_pages = math.ceil(total_items / size) if total_items > 0 else 1
        
        return {
            "items": books,
            "total": total_items,
            "page": page,
            "size": size,
            "pages": total_pages
        }
    
    def get_book_by_id(self, db: Session, book_id: UUID):
        book = self.book_repo.get_by_id(db, book_id)
        if not book:
            raise BookNotFoundException(book_id=str(book_id))
        return book
    
    def create_book(self, db: Session, book_in: BookCreate):
        return self.book_repo.create(db, book_in)
    
    def update_book(self, db: Session, book_id: UUID, book_in: BookUpdate):
        db_book = self.get_book_by_id(db, book_id)
        update_data = book_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
            
        db.commit()
        db.refresh(db_book)
        return db_book
    
    def delete_book(self, db: Session, book_id: UUID):
        db_book = self.get_book_by_id(db, book_id)
        try:
            db.delete(db_book)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise OnlineBookstoreException(
                message="Cannot delete book because it is linked to existing orders",
                status_code=400
            )
        return True