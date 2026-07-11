from app.exceptions import HotelNotFound, RoomNotFound
from app.schemas.rooms import RoomCreate, RoomUpdate
from app.services.base import BaseService


class RoomService(BaseService):
    async def _check_hotel_exists(self, hotel_id: int):
        if await self.db.hotels.get_by_id(hotel_id) is None:
            raise HotelNotFound

    async def list_rooms_by_hotel(self, hotel_id: int):
        await self._check_hotel_exists(hotel_id)
        return await self.db.rooms.list(hotel_id=hotel_id)

    async def create_room(self, data: RoomCreate, *, hotel_id: int):
        await self._check_hotel_exists(hotel_id)

        room = await self.db.rooms.add(**data.model_dump(), hotel_id=hotel_id)
        await self.db.commit()
        return room

    async def get_room(self, room_id: int):
        room = await self.db.rooms.get_by_id(room_id)
        if room is None:
            raise RoomNotFound
        return room

    async def update_room(self, room_id: int, data: RoomUpdate):
        room = await self.get_room(room_id)
        await self.db.rooms.update(room, data.model_dump(exclude_unset=True))
        await self.db.commit()
        return room

    async def delete_room(self, room_id: int):
        room = await self.get_room(room_id)
        await self.db.rooms.delete(room)
        await self.db.commit()
