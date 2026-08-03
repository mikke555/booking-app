from datetime import date

from app.models.bookings import Booking
from app.repositories.base import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    model = Booking

    async def count_overlapping(
        self, room_id: int, date_from: date, date_to: date
    ) -> int:
        return await self.count(
            Booking.room_id == room_id,
            Booking.date_from < date_to,
            Booking.date_to > date_from,
        )
