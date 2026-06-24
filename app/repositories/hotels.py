from app.models.hotels import Hotel
from app.repositories.base import BaseRepository
from app.schemas.hotels import HotelRead


class HotelRepository(BaseRepository[Hotel, HotelRead]):
    model = Hotel
    schema = HotelRead
