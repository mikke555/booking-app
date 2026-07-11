from app.exceptions import RoomNotFoundError
from app.models.bookings import Booking
from app.schemas.bookings import BookingCreate
from app.services.base import BaseService


class BookingService(BaseService):
    async def list_bookings(self) -> list[Booking]:
        return await self.db.bookings.list()

    async def get_user_bookings(self, user_id: int) -> list[Booking]:
        return await self.db.bookings.list(user_id=user_id)

    async def create_booking(self, data: BookingCreate, *, user_id: int) -> Booking:
        room = await self.db.rooms.get_by_id(data.room_id)
        if room is None:
            raise RoomNotFoundError

        booking = await self.db.bookings.add(
            user_id=user_id, price=room.price, **data.model_dump()
        )

        await self.db.commit()
        return booking
