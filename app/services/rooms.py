from sqlalchemy.exc import IntegrityError

from app.exceptions import (
    AmenityNotFoundError,
    HotelNotFoundError,
    RoomHasBookingsError,
    RoomNotFoundError,
)
from app.models.amenities import Amenity
from app.models.rooms import Room
from app.schemas.filters import DateRangeParams
from app.schemas.rooms import RoomCreate, RoomUpdate
from app.services.base import BaseService


class RoomService(BaseService):
    async def _check_hotel_exists(self, hotel_id: int) -> None:
        if await self.db.hotels.get_by_id(hotel_id) is None:
            raise HotelNotFoundError

    async def list_available_by_hotel(
        self,
        hotel_id: int,
        dates: DateRangeParams,
    ) -> list[Room]:
        await self._check_hotel_exists(hotel_id)
        return await self.db.rooms.list_available(
            hotel_id=hotel_id,
            date_from=dates.date_from,
            date_to=dates.date_to,
        )

    async def _resolve_amenities(self, amenities_ids: list[int]) -> list[Amenity]:
        if not amenities_ids:
            return []

        amenities = await self.db.amenities.list_by_ids(amenities_ids)
        missing = set(amenities_ids) - set(a.id for a in amenities)
        if missing:
            raise AmenityNotFoundError(f"Amenities not found: {sorted(missing)}")
        return amenities

    async def create_room(self, data: RoomCreate, *, hotel_id: int) -> Room:
        await self._check_hotel_exists(hotel_id)

        amenities = await self._resolve_amenities(data.amenities_ids)
        room = await self.db.rooms.add(
            **data.model_dump(exclude={"amenities_ids"}),
            hotel_id=hotel_id,
            amenities=amenities,
        )
        await self.db.commit()
        return room

    async def get_room(self, room_id: int) -> Room:
        room = await self.db.rooms.get_with_amenities(room_id)
        if room is None:
            raise RoomNotFoundError
        return room

    async def update_room(self, room_id: int, data: RoomUpdate) -> Room:
        room = await self.get_room(room_id)

        values = data.model_dump(exclude_unset=True, exclude_none=True)
        amenities_ids = values.pop("amenities_ids", None)
        if amenities_ids is not None:
            room.amenities = await self._resolve_amenities(amenities_ids)

        await self.db.rooms.update(room, **values)
        await self.db.commit()
        return room

    async def delete_room(self, room_id: int) -> None:
        room = await self.get_room(room_id)
        try:
            await self.db.rooms.delete(room)
            await self.db.commit()
        except IntegrityError as e:
            raise RoomHasBookingsError from e
