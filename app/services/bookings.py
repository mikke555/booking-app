from app.exceptions import RoomNotFound
from app.schemas.bookings import BookingCreate
from app.services.base import BaseService


class BookingService(BaseService):
    async def list_bookings(self):
        return await self.db.bookings.list()

    async def get_user_bookings(self, user_id: int):
        return await self.db.bookings.list(user_id=user_id)

    async def create_booking(self, data: BookingCreate, *, user_id: int):
        room = await self.db.rooms.get_by_id(data.room_id)
        if room is None:
            raise RoomNotFound

        booking = await self.db.bookings.add(
            user_id=user_id, price=room.price, **data.model_dump()
        )

        await self.db.commit()
        return booking
