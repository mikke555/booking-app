from pydantic import BaseModel


class Page[ItemT](BaseModel):
    items: list[ItemT]
    total: int
    page: int
    per_page: int
