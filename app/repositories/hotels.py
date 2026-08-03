from datetime import date

from sqlalchemy import ColumnElement

from app.models.hotels import Hotel
from app.repositories.base import BaseRepository
from app.repositories.queries import available_hotel_ids_stmt


class HotelRepository(BaseRepository[Hotel]):
    model = Hotel

    def _build_search_filters(
        self,
        *,
        date_from: date,
        date_to: date,
        name: str | None,
        location: str | None,
    ) -> list[ColumnElement[bool]]:
        available_hotel_ids = available_hotel_ids_stmt(date_from, date_to)

        filters = [Hotel.id.in_(available_hotel_ids)]
        if name is not None:
            filters.append(Hotel.name.ilike(f"%{name}%"))
        if location is not None:
            filters.append(Hotel.location.ilike(f"%{location}%"))

        return filters

    async def list_available(
        self,
        *,
        date_from: date,
        date_to: date,
        name: str | None = None,
        location: str | None = None,
        limit: int,
        offset: int,
    ) -> list[Hotel]:
        filters = self._build_search_filters(
            date_from=date_from, date_to=date_to, name=name, location=location
        )
        return await super().list(*filters, limit=limit, offset=offset)

    async def count_available(
        self,
        *,
        date_from: date,
        date_to: date,
        name: str | None = None,
        location: str | None = None,
    ) -> int:
        filters = self._build_search_filters(
            date_from=date_from, date_to=date_to, name=name, location=location
        )
        return await self.count(*filters)
