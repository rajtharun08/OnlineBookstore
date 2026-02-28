from sqlalchemy.orm import Session
from app.models.book import Book

class BookRepository:
    def get_all(self, db: Session, skip: int, limit: int):
        return db.query(Book).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, book_id: str):
        return db.query(Book).filter(Book.id == book_id).first()

    def create(self, db: Session, book_data: dict):
        db_book = Book(**book_data)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    
    def get_total_count(self, db: Session):
        return db.query(Book).count()
    
    def update(self, db: Session, db_book: Book, update_data: dict):
        for key, value in update_data.items():
            if value is not None:
                setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book

    def delete(self, db: Session, db_book: Book):
        db.delete(db_book)
        db.commit()
        return True