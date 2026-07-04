from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int, Query(10, ge=1, le=10)]

    @property
    def limit(self) -> int:
        return self.per_page

    @property
    def offset(self) -> int:
        return self.per_page * (self.page - 1)
