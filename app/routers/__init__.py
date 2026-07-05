from fastapi import APIRouter

from app.routers import health, hotels, rooms

master_router = APIRouter()
master_router.include_router(health.router)
master_router.include_router(hotels.router)
master_router.include_router(rooms.router)
