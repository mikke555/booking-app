from pydantic import BaseModel, Field


class RoomBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = None
    quantity: int = Field(ge=0)
    price: int = Field(ge=1)


class RoomCreate(RoomBase):
    pass


class RoomRead(RoomBase):
    id: int
    hotel_id: int


class RoomUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=120)
    description: str | None = None
    quantity: int | None = None
    price: int | None = None
