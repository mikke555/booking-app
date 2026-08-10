from app.exceptions import UserNotFoundError
from app.models.users import User
from app.schemas.filters import PaginationParams
from app.schemas.pagination import Page
from app.schemas.users import UserUpdate
from app.services.base import BaseService


class UserService(BaseService):
    async def list_users(self, pagination: PaginationParams) -> Page[User]:
        items = await self.db.users.list(
            limit=pagination.limit, offset=pagination.offset
        )
        total = await self.db.users.count()
        return Page[User](
            items=items,
            total=total,
            page=pagination.page,
            per_page=pagination.per_page,
        )

    async def get_user(self, user_id: int) -> User:
        user = await self.db.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = await self.get_user(user_id)

        await self.db.users.update(
            user, **data.model_dump(exclude_unset=True, exclude_none=True)
        )
        await self.db.commit()
        return user
