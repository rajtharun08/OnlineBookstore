from app.exceptions.custom_exceptions import BookNotFoundException
from sqlalchemy.orm import Session
from app.repositories.book_repository import BookRepository

class BookService:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def get_all_books(self, db: Session, page: int, size: int):
        skip = (page - 1) * size
        items = self.book_repo.get_all(db, skip, size)
        total_count = self.book_repo.get_total_count(db)
        total_pages = (total_count + size - 1) 
        return {
            "items": items,
            "total_count": total_count,
            "page": page,
            "size": size,
            "total_pages": total_pages
        }

    def get_book(self, db: Session, book_id: str):
        book_id=book_id.strip()
        book=self.book_repo.get_by_id(db, book_id)
        if not book:
            raise BookNotFoundException(book_id)
        return book

    def add_book(self, db: Session, book_in):
        return self.book_repo.create(db, book_in.model_dump())

    def update_book(self, db: Session, book_id: str, book_update):
        db_book = self.book_repo.get_by_id(db, book_id)
        if not db_book:
            raise BookNotFoundException(book_id)
        return self.book_repo.update(db, db_book, book_update.model_dump(exclude_unset=True))

    def remove_book(self, db: Session, book_id: str):
        db_book = self.book_repo.get_by_id(db, book_id)
        if not db_book:
            raise BookNotFoundException(book_id)
        return self.book_repo.delete(db, db_book)