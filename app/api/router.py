from fastapi import APIRouter
from app.api import router

api_router = APIRouter()

# Registering all sub-routers with their specific prefixes
app.include_router(api_router)