from app.exceptions import HotelNotFound
from app.schemas.hotels import HotelCreate, HotelUpdate
from app.schemas.pagination import PaginationParams
from app.utils.db_manager import DBManager


class HotelService:
    def __init__(self, db: DBManager):
        self.db = db

    async def get_hotel(self, id: int):
        hotel = await self.db.hotels.get_by_id(id)
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

    async def update_hotel(self, id: int, data: HotelUpdate):
        hotel = await self.db.hotels.update(id, data)
        if hotel is None:
            raise HotelNotFound
        await self.db.commit()
        return hotel

    async def delete_hotel(self, id: int) -> None:
        deleted = await self.db.hotels.delete(id)
        if not deleted:
            raise HotelNotFound
        await self.db.commit()
