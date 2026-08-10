from datetime import date

from sqlalchemy import ColumnElement

from app.models.hotels import Hotel
from app.repositories.base import BaseRepository
from app.repositories.queries import available_hotel_ids_stmt


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

        items = await self.list(*filters, limit=limit, offset=offset)
        total = await self.count(*filters)
        return items, total
