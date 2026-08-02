from datetime import date

from sqlalchemy.orm import selectinload

from app.models.rooms import Room
from app.repositories.base import BaseRepository
from app.repositories.queries import available_rooms_stmt


class RoomRepository(BaseRepository[Room]):
    model = Room

    async def get_with_amenities(self, room_id: int) -> Room | None:
        return await self.session.get(
            Room, room_id, options=[selectinload(Room.amenities)]
        )

    async def list_available(
        self, *, hotel_id: int, date_from: date, date_to: date
    ) -> list[Room]:
        stmt = (
            available_rooms_stmt(date_from, date_to, hotel_id=hotel_id)
            .options(selectinload(Room.amenities))
            .order_by(Room.id)
        )

        result = await self.session.execute(stmt)

        rooms = []
        for room, quantity_left in result.all():
            room.quantity_left = quantity_left
            rooms.append(room)
        return rooms
