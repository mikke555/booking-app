from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import AuthServiceDep
from app.schemas.auth import AccessToken
from app.schemas.users import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, auth: AuthServiceDep):
    return await auth.register(payload)


@router.post("/token", response_model=AccessToken)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth: AuthServiceDep
):
    return await auth.login(email=form_data.username, password=form_data.password)
