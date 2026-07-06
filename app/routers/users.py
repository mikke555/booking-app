from fastapi import APIRouter

from app.dependencies import CurrentUserDep
from app.schemas.users import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_me(user: CurrentUserDep):
    return user
