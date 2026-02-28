from app.exceptions.exception_handler import book_service_exception_handler,BookServiceException
from fastapi import FastAPI
from app.routers import book_router
from app.database.session import engine, Base
from app.models import book 

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bookstore Catalog Service",
    description="Microservice for managing book inventory and pricing",
    version="1.0.0"
)
app.add_exception_handler(BookServiceException, book_service_exception_handler)
app.include_router(book_router.router)

@app.get("/health", tags=["Health"])
def health_check():
    """
    Check if the Book Service and its Database are online.
    """
    return {
        "status": "online",
        "service": "book_service",
        "port": 8003
    }