from app.exceptions import HotelNotFoundError
from app.schemas.hotels import HotelCreate, HotelUpdate
from app.schemas.pagination import PaginationParams
from app.services.base import BaseService


class HotelService(BaseService):
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

    async def add_hotel(self, data: HotelCreate):
        hotel = await self.db.hotels.add(**data.model_dump())
        await self.db.commit()
        return hotel

    async def get_hotel(self, hotel_id: int):
        hotel = await self.db.hotels.get_by_id(hotel_id)
        if hotel is None:
            raise HotelNotFoundError
        return hotel

    async def update_hotel(self, hotel_id: int, data: HotelUpdate):
        hotel = await self.get_hotel(hotel_id)
        await self.db.hotels.update(hotel, data.model_dump(exclude_unset=True))
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int) -> None:
        hotel = await self.get_hotel(hotel_id)
        await self.db.hotels.delete(hotel)
        await self.db.commit()
