from app.schemas.book_schema import BookCreate,BookResponse,BookUpdate
from sqlalchemy.orm import Session
from app.models.book import Book
from uuid import UUID

class BookRepository:
    def get_all(self,db:Session,skip:int=0,limit:int=10):
        return db.query(Book).offset(skip).limit(limit).all()
    
    def get_by_id(self,db:Session,book_id:UUID):
        return db.query(Book).filter(Book.id==book_id).first()
    
    def create(self, db: Session, book_in: BookCreate):
        db_book = Book(
            title=book_in.title,
            author=book_in.author,
            description=book_in.description,
            price=book_in.price,
            stock_quantity=book_in.stock_quantity
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    
    def update(self, db: Session, db_book: Book, book_in: BookUpdate):
        # Update fields dynamically if they were provided
        update_data = book_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        
        db.commit()
        db.refresh(db_book)
        return db_book

    def delete(self, db: Session, db_book: Book):
        db.delete(db_book)
        db.commit()
        return True