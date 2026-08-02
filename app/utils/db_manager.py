from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.repositories.amenities import AmenityRepository
from app.repositories.bookings import BookingRepository
from app.repositories.hotels import HotelRepository
from app.repositories.rooms import RoomRepository
from app.repositories.users import UserRepository


class DBManager:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.hotels = HotelRepository(self.session)
        self.rooms = RoomRepository(self.session)
        self.users = UserRepository(self.session)
        self.bookings = BookingRepository(self.session)
        self.amenities = AmenityRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
