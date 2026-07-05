from app.exceptions import HotelNotFound
from app.schemas.hotels import HotelCreate, HotelUpdate
from app.schemas.pagination import PaginationParams
from app.services.base import BaseService


class HotelService(BaseService):
    async def get_hotel(self, hotel_id: int):
        hotel = await self.db.hotels.get_by_id(hotel_id)
        if hotel is None:
            raise HotelNotFound
        return hotel

    async def list_hotels(
        self,
        pagination: PaginationParams,
        *,
        name: str | None = None,
        location: str | None = None,
    ):
        return await self.db.hotels.list(
            name=name,
            location=location,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    async def add_hotel(self, hotel: HotelCreate):
        hotel = await self.db.hotels.add(hotel)
        await self.db.commit()
        return hotel

    async def update_hotel(self, hotel_id: int, data: HotelUpdate):
        hotel = await self.db.hotels.update(hotel_id, data)
        if hotel is None:
            raise HotelNotFound
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int) -> None:
        deleted = await self.db.hotels.delete(hotel_id)
        if not deleted:
            raise HotelNotFound
        await self.db.commit()
