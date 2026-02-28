from fastapi import FastAPI
from app.routers import order_router
from app.database.session import engine, Base
from app.models import order
from app.exceptions.custom_exceptions import OrderServiceException
from app.exceptions.exception_handler import order_exception_handler 
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bookstore Order Service",
    description="Handles transactions and inter-service stock coordination",
    version="1.0.0"
)
app.add_exception_handler(OrderServiceException, order_exception_handler)

app.include_router(order_router.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "service": "order_service",
        "port": 8004
    }