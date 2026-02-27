from fastapi import APIRouter
from app.api.routes import auth, books, users, orders

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(books.router,  tags=["Books"])
api_router.include_router(orders.router, tags=["Orders"])