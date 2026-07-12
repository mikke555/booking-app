from app.exceptions import HotelNotFoundError
from app.models.hotels import Hotel
from app.schemas.hotels import HotelCreate, HotelFilterParams, HotelUpdate
from app.services.base import BaseService


class HotelService(BaseService):
    async def list_hotels(self, filters: HotelFilterParams) -> list[Hotel]:
        return await self.db.hotels.list_available(
            name=filters.name,
            location=filters.location,
            date_from=filters.date_from,
            date_to=filters.date_to,
            limit=filters.limit,
            offset=filters.offset,
        )

    async def add_hotel(self, data: HotelCreate) -> Hotel:
        hotel = await self.db.hotels.add(**data.model_dump())
        await self.db.commit()
        return hotel

    async def get_hotel(self, hotel_id: int) -> Hotel:
        hotel = await self.db.hotels.get_by_id(hotel_id)
        if hotel is None:
            raise HotelNotFoundError
        return hotel

    async def update_hotel(self, hotel_id: int, data: HotelUpdate) -> Hotel:
        hotel = await self.get_hotel(hotel_id)
        await self.db.hotels.update(hotel, data.model_dump(exclude_unset=True))
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int) -> None:
        hotel = await self.get_hotel(hotel_id)
        await self.db.hotels.delete(hotel)
        await self.db.commit()
