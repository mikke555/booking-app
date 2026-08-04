from fastapi import APIRouter, Depends

from app.dependencies import (
    CurrentUserDep,
    PaginationDep,
    UserServiceDep,
    get_current_admin,
)
from app.schemas.pagination import Page
from app.schemas.users import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=Page[UserRead],
    dependencies=[Depends(get_current_admin)],
)
async def list_users(service: UserServiceDep, pagination: PaginationDep):
    return await service.list_users(pagination)


@router.get("/me", response_model=UserRead)
async def get_me(user: CurrentUserDep):
    return user


@router.get(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(get_current_admin)],
)
async def get_user(user_id: int, service: UserServiceDep):
    return await service.get_user(user_id)


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(get_current_admin)],
)
async def update_user(user_id: int, payload: UserUpdate, service: UserServiceDep):
    return await service.update_user(user_id, payload)
