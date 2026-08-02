from app.exceptions import UserNotFoundError
from app.models.users import User
from app.services.base import BaseService


class UserService(BaseService):
    async def set_active(self, user_id: int, *, is_active: bool) -> User:
        user = await self.db.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError

        await self.db.users.update(user, {"is_active": is_active})
        await self.db.commit()
        return user
