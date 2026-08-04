from app.exceptions import (
    BookingNotFoundError,
    RoomNotAvailableError,
    RoomNotFoundError,
)
from app.models.bookings import Booking
from app.schemas.bookings import BookingAdminRead, BookingCreate, BookingRead
from app.schemas.filters import PaginationParams
from app.schemas.pagination import Page
from app.services.base import BaseService


class BookingService(BaseService):
    async def list_bookings(
        self, pagination: PaginationParams
    ) -> Page[BookingAdminRead]:
        items = await self.db.bookings.list(
            limit=pagination.limit,
            offset=pagination.offset,
            order_by=Booking.id.desc(),
        )
        total = await self.db.bookings.count()
        return Page[BookingAdminRead](
            items=items,
            total=total,
            page=pagination.page,
            per_page=pagination.per_page,
        )

    async def get_user_bookings(
        self, user_id: int, pagination: PaginationParams
    ) -> Page[BookingRead]:
        items = await self.db.bookings.list(
            limit=pagination.limit,
            offset=pagination.offset,
            order_by=Booking.id.desc(),
            user_id=user_id,
        )
        total = await self.db.bookings.count(user_id=user_id)
        return Page[BookingRead](
            items=items,
            total=total,
            page=pagination.page,
            per_page=pagination.per_page,
        )

    async def create_booking(self, data: BookingCreate, *, user_id: int) -> Booking:
        room = await self.db.rooms.get_by_id(data.room_id, for_update=True)
        if room is None:
            raise RoomNotFoundError

        booked = await self.db.bookings.count_overlapping(
            room_id=room.id,
            date_from=data.date_from,
            date_to=data.date_to,
        )
        if booked >= room.quantity:
            raise RoomNotAvailableError

        booking = await self.db.bookings.add(
            user_id=user_id, price=room.price, **data.model_dump()
        )

        await self.db.commit()
        return booking

    async def cancel_booking(self, *, booking_id: int, owner_id: int | None) -> Booking:
        booking = await self.db.bookings.cancel(
            booking_id=booking_id, owner_id=owner_id
        )

        if booking is None:
            raise BookingNotFoundError

        await self.db.commit()
        return booking
