from datetime import date
from typing import Any

from sqlalchemy import Row

from app.models.rooms import Room
from app.repositories.base import BaseRepository
from app.repositories.queries import available_rooms_stmt


class RoomRepository(BaseRepository[Room]):
    model = Room

    async def list_available(
        self, *, hotel_id: int, date_from: date, date_to: date
    ) -> list[Row[Any]]:
        stmt = available_rooms_stmt(
            date_from,
            date_to,
            hotel_id=hotel_id,
        ).order_by(Room.id)

        result = await self.session.execute(stmt)
        return list(result.all())
