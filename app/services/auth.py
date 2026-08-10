import logging

from sqlalchemy.exc import IntegrityError

from app.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserDeactivatedError,
)
from app.models.users import User
from app.schemas.auth import AccessToken
from app.schemas.users import UserCreate
from app.services.base import BaseService
from app.utils.security import (
    DUMMY_HASH,
    create_access_token,
    hash_password,
    verify_password,
)

logger = logging.getLogger(__name__)


class AuthService(BaseService):
    async def register(self, data: UserCreate) -> User:
        try:
            user = await self.db.users.add(
                email=data.email.lower(),
                hashed_password=hash_password(data.password),
            )
            await self.db.commit()
            return user

        except IntegrityError as e:
            raise UserAlreadyExistsError from e

    async def login(self, email: str, password: str) -> AccessToken:
        user = await self.db.users.get_one_by_filter(email=email.lower())

        if user is None:
            verify_password(password, DUMMY_HASH)
            logger.warning("Failed login for %s: unknown email", email)
            raise InvalidCredentialsError

        if not verify_password(password, user.hashed_password):
            logger.warning("Failed login for %s: wrong password", email)
            raise InvalidCredentialsError

        if not user.is_active:
            logger.warning("Login attempt for deactivated account %s", email)
            raise UserDeactivatedError

        return AccessToken(access_token=create_access_token(user.id))
