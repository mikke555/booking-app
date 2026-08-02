from pydantic import BaseModel, Field


class AmenityBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class AmenityCreate(AmenityBase):
    pass


class AmenityRead(AmenityBase):
    id: int
