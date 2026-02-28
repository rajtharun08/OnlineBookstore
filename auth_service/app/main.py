from app.exceptions.custom_exception import AuthServiceException
from app.exceptions.exception_handler import auth_exception_handler
from fastapi import FastAPI
from app.routers import auth_router
from app.database.session import create_tables, engine, Base

app = FastAPI(title="Bookstore Auth Service")
create_tables()
app.include_router(auth_router.router)
app.add_exception_handler(AuthServiceException, auth_exception_handler)
@app.get("/health")
def health():
    return {"status": "Auth Service Healthy"}