from app.models.amenities import Amenity
from app.repositories.base import BaseRepository


class AmenityRepository(BaseRepository[Amenity]):
    model = Amenity
