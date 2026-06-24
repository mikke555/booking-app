from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends

from app.database import session_factory
from app.services.hotels import HotelService
from app.utils.db_manager import DBManager


async def get_db_manager() -> AsyncIterator[DBManager]:
    async with DBManager(session_factory) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db_manager)]


def get_hotel_service(db: DBDep) -> HotelService:
    return HotelService(db)


HotelServiceDep = Annotated[HotelService, Depends(get_hotel_service)]
