from app.models.hotels import Hotel
from app.repositories.base import BaseRepository


class HotelRepository(BaseRepository[Hotel]):
    model = Hotel

    async def list(
        self,
        *,
        name: str | None = None,
        location: str | None = None,
        limit: int,
        offset: int,
    ) -> list[Hotel]:
        filters = []
        if name is not None:
            filters.append(Hotel.name.ilike(f"%{name}%"))

        if location is not None:
            filters.append(Hotel.location.ilike(f"%{location}%"))

        return await super().list(*filters, limit=limit, offset=offset)
