from app.models.rooms import Room
from app.repositories.base import BaseRepository
from app.schemas.rooms import RoomRead


class RoomRepository(BaseRepository[Room, RoomRead]):
    model = Room
    schema = RoomRead
