from datetime import date

from sqlalchemy import func, select

from app.models.bookings import Booking
from app.repositories.base import BaseRepository


class BookingRepository(BaseRepository):
    model = Booking

    async def count_overlapping(
        self, room_id: int, date_from: date, date_to: date
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(Booking)
            .where(
                Booking.room_id == room_id,
                Booking.date_from < date_to,
                Booking.date_to > date_from,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
