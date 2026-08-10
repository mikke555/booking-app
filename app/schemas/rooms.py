from typing import TYPE_CHECKING

from fastapi.openapi.models import Example
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.amenities import AmenityRead

if TYPE_CHECKING:
    from app.models.rooms import Room


class RoomBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = None
    quantity: int = Field(gt=0)
    price: int = Field(gt=0)


class RoomCreate(RoomBase):
    amenities_ids: list[int] = []


class RoomReadBase(BaseModel):
    id: int
    hotel_id: int
    title: str
    description: str | None
    price: int
    amenities: list[AmenityRead] = []

    model_config = ConfigDict(from_attributes=True)


class RoomRead(RoomReadBase):
    quantity: int


class RoomReadAvailable(RoomReadBase):
    quantity_left: int

    @classmethod
    def from_row(cls, room: Room, quantity_left: int) -> RoomReadAvailable:
        return cls(
            **RoomReadBase.model_validate(room).model_dump(),
            quantity_left=quantity_left,
        )


class RoomUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=120)
    description: str | None = None
    quantity: int | None = Field(None, gt=0)
    price: int | None = Field(None, gt=0)
    amenities_ids: list[int] | None = None


room_create_examples: dict[str, Example] = {
    "single": Example(
        summary="Single room",
        value={
            "title": "Single Room",
            "description": "Compact room with a single bed",
            "quantity": 2,
            "price": 100,
        },
    ),
    "double": Example(
        summary="Double room",
        value={
            "title": "Double Room",
            "description": "Room with a double bed and city view",
            "quantity": 1,
            "price": 250,
        },
    ),
}
