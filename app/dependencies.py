from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer

from app.database import session_factory
from app.exceptions import ForbiddenError, InvalidTokenError, UserDeactivatedError
from app.models.users import User
from app.schemas.filters import DateRangeParams
from app.schemas.hotels import HotelFilterParams
from app.services.amenities import AmenityService
from app.services.auth import AuthService
from app.services.bookings import BookingService
from app.services.hotels import HotelService
from app.services.rooms import RoomService
from app.services.users import UserService
from app.utils.db_manager import DBManager
from app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


DateRangeDep = Annotated[DateRangeParams, Query()]
HotelFilterDep = Annotated[HotelFilterParams, Query()]


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


def get_booking_service(db: DBDep) -> BookingService:
    return BookingService(db)


BookingServiceDep = Annotated[BookingService, Depends(get_booking_service)]


def get_amenity_service(db: DBDep) -> AmenityService:
    return AmenityService(db)


AmenityServiceDep = Annotated[AmenityService, Depends(get_amenity_service)]


def get_user_service(db: DBDep) -> UserService:
    return UserService(db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: DBDep
) -> User:
    user_id = decode_access_token(token)
    user = await db.users.get_by_id(user_id)
    if user is None:
        raise InvalidTokenError
    if not user.is_active:
        raise UserDeactivatedError
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_admin(user: CurrentUserDep) -> User:
    if not user.is_admin:
        raise ForbiddenError
    return user
