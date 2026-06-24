from fastapi import APIRouter

from app.routers import health, hotels

master_router = APIRouter()
master_router.include_router(health.router)
master_router.include_router(hotels.router)
