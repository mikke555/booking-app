from sqlalchemy.exc import IntegrityError

from app.exceptions import AmenityAlreadyExistsError, AmenityNotFoundError
from app.models.amenities import Amenity
from app.schemas.amenities import AmenityCreate
from app.services.base import BaseService


class AmenityService(BaseService):
    async def list_amenities(self) -> list[Amenity]:
        return await self.db.amenities.list()

    async def add_amenity(self, data: AmenityCreate) -> Amenity:
        try:
            amenity = await self.db.amenities.add(**data.model_dump())
            await self.db.commit()
            return amenity
        except IntegrityError as e:
            raise AmenityAlreadyExistsError from e

    async def get_amenity(self, amenity_id: int) -> Amenity:
        amenity = await self.db.amenities.get_by_id(amenity_id)
        if amenity is None:
            raise AmenityNotFoundError
        return amenity

    async def update_amenity(self, amenity_id: int, data: AmenityCreate) -> Amenity:
        amenity = await self.get_amenity(amenity_id)
        try:
            await self.db.amenities.update(amenity, data.model_dump())
            await self.db.commit()
            return amenity
        except IntegrityError as e:
            raise AmenityAlreadyExistsError from e

    async def delete_amenity(self, amenity_id: int) -> None:
        amenity = await self.get_amenity(amenity_id)
        await self.db.amenities.delete(amenity)
        await self.db.commit()
