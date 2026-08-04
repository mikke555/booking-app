from datetime import date

from sqlalchemy import func, update

from app.models.bookings import Booking
from app.repositories.base import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    model = Booking

    async def cancel(self, booking_id: int, user_id: int) -> Booking | None:
        stmt = (
            update(Booking)
            .where(
                Booking.id == booking_id,
                Booking.user_id == user_id,
            )
            .values(
                cancelled_at=func.coalesce(
                    Booking.cancelled_at,
                    func.now(),
                )
            )
            .returning(Booking)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def count_overlapping(
        self, room_id: int, date_from: date, date_to: date
    ) -> int:
        return await self.count(
            Booking.room_id == room_id,
            Booking.date_from < date_to,
            Booking.date_to > date_from,
        )
