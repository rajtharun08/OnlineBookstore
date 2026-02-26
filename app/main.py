import logging
# --- FIX FOR PASSLIB/BCRYPT COMPATIBILITY ---
import bcrypt

# This tricks passlib into seeing the version info it expects
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type('About', (object,), {'__version__': bcrypt.__version__})
# --------------------------------------------
from fastapi import FastAPI
from app.api.routes import books,auth
from app.models.base import Base
from app.core.database import engine
from app.middleware.logging_middleware import LoggingMiddleware
from app.exceptions.custom_exceptions import OnlineBookstoreException 
from app.exceptions.exception_handlers import bookstore_exception_handler 

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Bookstore API",
    description="A professional API for managing book inventory"
)
app.add_exception_handler(OnlineBookstoreException, bookstore_exception_handler)
app.add_middleware(LoggingMiddleware)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(books.router, tags=["Books"])

@app.get("/")
def root():
    return {"message": "Welcome to the Online Bookstore API! Visit /docs for the Swagger UI."}