from app.routers import health
from fastapi import APIRouter

master_router = APIRouter()
master_router.include_router(health.router)
