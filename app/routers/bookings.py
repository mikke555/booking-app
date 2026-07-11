from fastapi import APIRouter, status

from app.dependencies import BookingServiceDep, CurrentUserDep
from app.schemas.bookings import BookingCreate, BookingRead

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", response_model=list[BookingRead])
async def get_bookings(service: BookingServiceDep):
    return await service.list_bookings()


@router.get("/me", response_model=list[BookingRead])
async def get_my_bookings(service: BookingServiceDep, user: CurrentUserDep):
    return await service.get_user_bookings(user.id)


@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def create_booking(
    payload: BookingCreate, service: BookingServiceDep, user: CurrentUserDep
):
    return await service.create_booking(payload, user_id=user.id)
