from app.schemas.book_schema import BookResponse,BookCreate,BookUpdate
from app.repositories.book_repository import BookRepository
from fastapi import HTTPException 
from sqlalchemy.orm import Session
from uuid import UUID
from app.exceptions.custom_exceptions import BookNotFoundException,OnlineBookstoreException
from app.models.book import Book

class BookService:
    def __init__(self,book_repo:BookRepository):
        self.book_repo=book_repo
    
    def get_all_books(self, db: Session, skip: int = 0, limit: int = 10):
        return self.book_repo.get_all(db, skip=skip, limit=limit)
    
    def get_book_by_id(self,db:Session,book_id:UUID):
        book = self.book_repo.get_by_id(db, book_id)
        if not book:
            raise BookNotFoundException(book_id=str(book_id))
        return book
    
    def create_book(self,db:Session,book_in:BookCreate):
        return self.book_repo.create(db,book_in)
    
    def update_book(self, db: Session, book_id: UUID, book_in: BookUpdate):
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise OnlineBookstoreException(message="Book not found", status_code=404)
        update_data = book_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
            
        db.commit()
        db.refresh(db_book)
        return db_book

    def delete_book(self, db: Session, book_id: UUID):
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            raise OnlineBookstoreException(message="Book not found", status_code=404)
        
        db.delete(db_book)
        db.commit()
        return True
