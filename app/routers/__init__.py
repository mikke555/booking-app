from fastapi import APIRouter

from app.routers import auth, bookings, health, hotels, rooms, users

master_router = APIRouter()
master_router.include_router(health.router)
master_router.include_router(auth.router)
master_router.include_router(hotels.router)
master_router.include_router(rooms.router)
master_router.include_router(users.router)
master_router.include_router(bookings.router)
