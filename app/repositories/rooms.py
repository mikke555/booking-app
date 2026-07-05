from app.models.rooms import Room
from app.repositories.base import BaseRepository


class RoomRepository(BaseRepository[Room]):
    model = Room
