from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import BookServiceException

async def book_service_exception_handler(request: Request, exc: BookServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_type": exc.__class__.__name__,
            "message": exc.message
        },
    )