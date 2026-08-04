from app.models.amenities import Amenity
from app.repositories.base import BaseRepository


class AmenityRepository(BaseRepository[Amenity]):
    model = Amenity

    async def list_by_ids(self, ids: list[int]) -> list[Amenity]:
        if not ids:
            return []
        return await self.list(Amenity.id.in_(ids))
