from datetime import date

from sqlalchemy import ColumnElement

from app.models.hotels import Hotel
from app.repositories.availability import available_hotel_ids_stmt
from app.repositories.base import BaseRepository


class HotelRepository(BaseRepository[Hotel]):
    model = Hotel

    async def search(
        self,
        *,
        date_from: date,
        date_to: date,
        name: str | None = None,
        location: str | None = None,
        limit: int,
        offset: int,
    ) -> tuple[list[Hotel], int]:
        filters: list[ColumnElement[bool]] = [
            Hotel.id.in_(available_hotel_ids_stmt(date_from, date_to))
        ]
        if name is not None:
            filters.append(Hotel.name.ilike(f"%{name}%"))
        if location is not None:
            filters.append(Hotel.location.ilike(f"%{location}%"))

        return await self.list_and_count(*filters, limit=limit, offset=offset)
