from datetime import date

from app.models.hotels import Hotel
from app.models.rooms import Room
from app.repositories.base import BaseRepository
from app.repositories.queries import available_rooms_stmt


class HotelRepository(BaseRepository[Hotel]):
    model = Hotel

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
        available_rooms = available_rooms_stmt(date_from, date_to)
        available_hotel_ids = available_rooms.with_only_columns(Room.hotel_id)

        filters = [Hotel.id.in_(available_hotel_ids)]
        if name is not None:
            filters.append(Hotel.name.ilike(f"%{name}%"))
        if location is not None:
            filters.append(Hotel.location.ilike(f"%{location}%"))

        return await super().list(*filters, limit=limit, offset=offset)
