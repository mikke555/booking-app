from app.exceptions import HotelNotFound, RoomNotFound
from app.schemas.rooms import RoomCreate, RoomUpdate
from app.services.base import BaseService


class RoomService(BaseService):
    async def _check_hotel_exists(self, hotel_id: int):
        hotel = await self.db.hotels.get_by_id(hotel_id)
        if hotel is None:
            raise HotelNotFound

    async def list_rooms_by_hotel(self, hotel_id: int):
        await self._check_hotel_exists(hotel_id)
        return await self.db.rooms.list(hotel_id=hotel_id)

    async def create_room(self, hotel_id: int, data: RoomCreate):
        await self._check_hotel_exists(hotel_id)

        room = await self.db.rooms.add(data, hotel_id=hotel_id)
        await self.db.commit()
        return room

    async def get_room(self, room_id: int):
        room = await self.db.rooms.get_by_id(room_id)
        if room is None:
            raise RoomNotFound
        return room

    async def update_room(self, room_id: int, data: RoomUpdate):
        room = await self.db.rooms.update(room_id, data)
        if room is None:
            raise RoomNotFound
        await self.db.commit()
        return room

    async def delete_room(self, room_id: int):
        deleted = await self.db.rooms.delete(room_id)
        if not deleted:
            raise RoomNotFound
        await self.db.commit()
