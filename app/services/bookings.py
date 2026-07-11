from app.services.base import BaseService


class BookingService(BaseService):
    async def list_bookings(self):
        return await self.db.bookings.list()
