from app.models.hotels import Hotel
from app.repositories.base import BaseRepository
from app.schemas.hotels import HotelRead


class HotelRepository(BaseRepository[Hotel, HotelRead]):
    model = Hotel
    schema = HotelRead

    async def list(
        self,
        name: str | None = None,
        location: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[HotelRead]:
        filters = []
        if name is not None:
            filters.append(Hotel.name.ilike(f"%{name}%"))

        if location is not None:
            filters.append(Hotel.location.ilike(f"%{location}%"))

        return await super().list(*filters, limit=limit, offset=offset)
