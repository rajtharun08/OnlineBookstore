from sqlalchemy.orm import Session
from app.repositories.book_repository import BookRepository

class BookService:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def list_books(self, db: Session):
        return self.book_repo.get_all(db)

    def get_book(self, db: Session, book_id: str):
        return self.book_repo.get_by_id(db, book_id)

    def add_book(self, db: Session, book_in):
        return self.book_repo.create(db, book_in.model_dump())

    def update_book(self, db: Session, book_id: str, book_update):
        db_book = self.book_repo.get_by_id(db, book_id)
        if not db_book:
            return None
        return self.book_repo.update(db, db_book, book_update.model_dump(exclude_unset=True))

    def remove_book(self, db: Session, book_id: str):
        db_book = self.book_repo.get_by_id(db, book_id)
        if not db_book:
            return False
        return self.book_repo.delete(db, db_book)