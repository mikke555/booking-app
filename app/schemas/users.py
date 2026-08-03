from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr = Field(min_length=6, max_length=64)
    password: str = Field(min_length=8, max_length=64)


class UserUpdate(BaseModel):
    is_active: bool | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
