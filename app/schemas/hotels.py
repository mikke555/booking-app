from pydantic import BaseModel, Field


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


hotel_create_examples = {
    "tallinn": {
        "summary": "Tallinn hotel",
        "value": {
            "name": "Nordic Hotel Forum",
            "location": "Tallinn",
        },
    },
    "dubai": {
        "summary": "Dubai hotel",
        "value": {
            "name": "Burj Al Arab",
            "location": "Dubai",
        },
    },
}
