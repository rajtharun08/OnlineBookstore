from fastapi import FastAPI
from app.routers import auth_router
from app.database.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore Auth Service")
app.include_router(auth_router.router)

@app.get("/health")
def health():
    return {"status": "Auth Service Healthy"}