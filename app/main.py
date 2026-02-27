from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from app.api.router import api_router
from app.core.database import engine
from app.models.base import Base
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.cors import setup_cors
from app.exceptions.custom_exceptions import OnlineBookstoreException
from app.exceptions.exception_handlers import global_exception_handler, bookstore_exception_handler



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Bookstore API")
app.add_exception_handler(OnlineBookstoreException, bookstore_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

setup_cors(app)

app.add_middleware(LoggingMiddleware)

app.include_router(api_router)
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Online Bookstore API. Visit /docs for Swagger UI."}

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "Bookstore API is healthy"}