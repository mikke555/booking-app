from fastapi import APIRouter, Depends, status

from app.dependencies import (
    BookingServiceDep,
    CurrentUserDep,
    PaginationDep,
    get_current_admin,
)
from app.schemas.bookings import BookingAdminRead, BookingCreate, BookingRead
from app.schemas.pagination import Page

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get(
    "/",
    response_model=Page[BookingAdminRead],
    dependencies=[Depends(get_current_admin)],
)
async def get_bookings(service: BookingServiceDep, pagination: PaginationDep):
    return await service.list_bookings(pagination)


@router.get("/me", response_model=Page[BookingRead])
async def get_my_bookings(
    service: BookingServiceDep, user: CurrentUserDep, pagination: PaginationDep
):
    return await service.get_user_bookings(user.id, pagination)


@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def create_booking(
    payload: BookingCreate, service: BookingServiceDep, user: CurrentUserDep
):
    return await service.create_booking(payload, user_id=user.id)


@router.post("/{booking_id}/cancel", response_model=BookingRead)
async def cancel_booking(
    booking_id: int, service: BookingServiceDep, user: CurrentUserDep
):
    return await service.cancel_booking(
        booking_id=booking_id,
        owner_id=None if user.is_admin else user.id,
    )
