from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import OnlineBookstoreException

async def bookstore_exception_handler(request: Request, exc: OnlineBookstoreException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.status_code,
            "message": exc.message
        }
    )