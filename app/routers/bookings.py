from fastapi import APIRouter

from app.dependencies import BookingServiceDep

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/")
async def get_bookings(service: BookingServiceDep):
    return await service.list_bookings()
