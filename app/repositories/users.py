from app.models.users import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User
