from fastapi.openapi.models import Example
from pydantic import BaseModel, ConfigDict, Field
from pydantic.json_schema import SkipJsonSchema

from app.schemas.filters import DateRangeFilter, PaginationFilter


class HotelFilterParams(BaseModel, PaginationFilter, DateRangeFilter):
    name: str | SkipJsonSchema[None] = Field(None, min_length=1, max_length=100)
    location: str | SkipJsonSchema[None] = Field(None, min_length=1, max_length=100)


class HotelBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=100)


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    location: str | None = Field(None, min_length=1, max_length=100)


class HotelRead(HotelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


hotel_create_examples: dict[str, Example] = {
    "tallinn": Example(
        summary="Tallinn hotel",
        value={
            "name": "Nordic Hotel Forum",
            "location": "Tallinn",
        },
    ),
    "dubai": Example(
        summary="Dubai hotel",
        value={
            "name": "Burj Al Arab",
            "location": "Dubai",
        },
    ),
}
