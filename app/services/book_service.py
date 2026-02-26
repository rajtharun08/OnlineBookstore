from app.schemas.book_schema import BookResponse,BookCreate
from app.repositories.book_repository import BookRepository
from fastapi import HTTPException 
from sqlalchemy.orm import Session
from uuid import UUID

class BookService:
    def __init__(self,book_repo:BookRepository):
        self.book_repo=book_repo
    
    def get_all_books(self,db:Session):
        return self.book_repo.get_all(db)
    
    def get_book_by_id(self,db:Session,book_id:UUID):
        return self.book_repo.get_by_id(db,UUID)
    
    def create_book(self,db:Session,book_in:BookCreate):
        return self.book_repo.create(db,book_in)
    
