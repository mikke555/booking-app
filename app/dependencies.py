from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.database import session_factory
from app.exceptions import InvalidToken
from app.models.users import User
from app.schemas.pagination import PaginationParams
from app.services.auth import AuthService
from app.services.hotels import HotelService
from app.services.rooms import RoomService
from app.utils.db_manager import DBManager
from app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


PaginationDep = Annotated[PaginationParams, Depends()]


async def get_db_manager() -> AsyncIterator[DBManager]:
    async with DBManager(session_factory) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db_manager)]


def get_hotel_service(db: DBDep) -> HotelService:
    return HotelService(db)


HotelServiceDep = Annotated[HotelService, Depends(get_hotel_service)]


def get_room_service(db: DBDep) -> RoomService:
    return RoomService(db)


RoomServiceDep = Annotated[RoomService, Depends(get_room_service)]


def get_auth_service(db: DBDep) -> AuthService:
    return AuthService(db)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: DBDep
) -> User:
    user_id = decode_access_token(token)
    user = await db.users.get_by_id(user_id)
    if user is None:
        raise InvalidToken
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
