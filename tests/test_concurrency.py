"""Concurrency test for BookingService.create_booking (FOR UPDATE row lock).

The lock only serializes separate connections, so the usual rollback-based
fixtures don't apply here.
"""

import asyncio
from datetime import date

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings
from app.database import session_factory
from app.exceptions import RoomNotAvailableError
from app.models.bookings import Booking
from app.models.hotels import Hotel
from app.models.users import User
from app.schemas.bookings import BookingCreate
from app.services.bookings import BookingService
from app.utils.db_manager import DBManager
from tests.const import DATE_FROM, DATE_TO

ATTEMPTS = 10


@pytest.fixture
async def race_sessionmaker():
    """Own engine with an empty pool.

    Every attempt dials a fresh connection, so nobody gets a head start by
    inheriting one from the shared app engine.
    """

    engine = create_async_engine(settings.database_url)
    yield async_sessionmaker(bind=engine, expire_on_commit=False)
    await engine.dispose()


@pytest.fixture
async def committed_data():
    """Commit test data for real so that other connections can see it"""

    async with DBManager(session_factory) as db:
        user = await db.users.add(email="race@example.com", hashed_password="n/a")
        hotel = await db.hotels.add(name="Race Hotel", location="Nowhere")
        room = await db.rooms.add(
            hotel_id=hotel.id, title="Last Room", price=100, quantity=1
        )
        await db.commit()

    yield user.id, room.id

    async with DBManager(session_factory) as db:
        await db.session.execute(delete(Booking).where(Booking.room_id == room.id))
        await db.session.execute(delete(Hotel).where(Hotel.id == hotel.id))
        await db.session.execute(delete(User).where(User.id == user.id))
        await db.commit()


async def test_concurrent_booking_no_oversell(committed_data, race_sessionmaker):
    user_id, room_id = committed_data

    async def try_book() -> bool:
        payload = BookingCreate(
            room_id=room_id,
            date_from=date.fromisoformat(DATE_FROM),
            date_to=date.fromisoformat(DATE_TO),
        )
        # Fresh connection per attempt
        async with DBManager(race_sessionmaker) as db:
            try:
                await BookingService(db).create_booking(payload, user_id=user_id)
                return True
            except RoomNotAvailableError:
                return False

    # Expected result: exactly one True among ATTEMPTS
    results = await asyncio.gather(*(try_book() for _ in range(ATTEMPTS)))
    assert results.count(True) == 1

    async with DBManager(session_factory) as db:
        assert await db.bookings.count(room_id=room_id) == 1
