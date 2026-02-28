from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exception import AuthServiceException

async def auth_exception_handler(request: Request, exc: AuthServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_type": exc.__class__.__name__,
            "message": exc.message
        }
    )