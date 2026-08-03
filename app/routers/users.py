from fastapi import APIRouter, Depends

from app.dependencies import CurrentUserDep, UserServiceDep, get_current_admin
from app.schemas.users import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=list[UserRead],
    dependencies=[Depends(get_current_admin)],
)
async def list_users(service: UserServiceDep):
    return await service.list_users()


@router.get("/me", response_model=UserRead)
async def get_me(user: CurrentUserDep):
    return user


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(get_current_admin)],
)
async def update_user(user_id: int, payload: UserUpdate, service: UserServiceDep):
    return await service.update_user(user_id, payload)
