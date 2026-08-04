from pydantic import BaseModel, ConfigDict


class Page[ItemT](BaseModel):
    items: list[ItemT]
    total: int
    page: int
    per_page: int

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
