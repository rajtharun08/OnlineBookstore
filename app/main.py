from fastapi import FastAPI
from app.api.routes import books
from app.models.base import Base
from app.core.database import engine
from app.middleware.logging_middleware import LoggingMiddleware
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Bookstore API",
    description="A professional API for managing book inventory"
)

app.add_middleware(LoggingMiddleware)

app.include_router(books.router, prefix="/books", tags=["Books"])

@app.get("/")
def root():
    return {"message": "Welcome to the Online Bookstore API! Visit /docs for the Swagger UI."}