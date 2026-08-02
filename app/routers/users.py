from fastapi import APIRouter, Depends

from app.dependencies import CurrentUserDep, UserServiceDep, get_current_admin
from app.schemas.users import UserRead, UserSetActive

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_me(user: CurrentUserDep):
    return user


@router.patch(
    "/{user_id}/activation",
    response_model=UserRead,
    dependencies=[Depends(get_current_admin)],
    description="Activate or deactivate a user account.",
)
async def set_user_activation(
    user_id: int, payload: UserSetActive, service: UserServiceDep
):
    return await service.set_active(user_id, is_active=payload.is_active)
