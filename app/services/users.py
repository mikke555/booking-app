from app.exceptions import UserNotFoundError
from app.models.users import User
from app.schemas.users import UserUpdate
from app.services.base import BaseService


class UserService(BaseService):
    async def list_users(self) -> list[User]:
        return await self.db.users.list()

    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = await self.db.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError

        await self.db.users.update(user, data.model_dump(exclude_unset=True))
        await self.db.commit()
        return user
