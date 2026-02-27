from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from app.api.router import api_router
from app.core.database import engine
from app.models.base import Base
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.cors import setup_cors
from app.exceptions.custom_exceptions import OnlineBookstoreException
from app.exceptions import exception_handlers



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Bookstore API")
@app.exception_handler(OnlineBookstoreException)
async def custom_exception_handler(request: Request, exc: OnlineBookstoreException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "code": "BOOKSTORE_ERROR"},
    )

setup_cors(app)

app.add_middleware(LoggingMiddleware)

app.include_router(api_router)
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Online Bookstore API. Visit /docs for Swagger UI."}

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "Bookstore API is healthy"}