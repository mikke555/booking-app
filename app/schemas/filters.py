from datetime import date
from typing import Annotated, Self

from pydantic import BaseModel, Field, model_validator


class DateRangeFilter:
    """Mixin with date range fields for query models."""

    date_from: Annotated[date, Field(json_schema_extra={"example": "2026-07-12"})]
    date_to: Annotated[date, Field(json_schema_extra={"example": "2026-07-15"})]

    @model_validator(mode="after")
    def check_dates(self) -> Self:
        if self.date_from >= self.date_to:
            raise ValueError("date_from must be earlier than date_to")
        return self


class PaginationFilter:
    """Mixin with pagination fields for query models."""

    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)

    @property
    def limit(self) -> int:
        return self.per_page

    @property
    def offset(self) -> int:
        return self.per_page * (self.page - 1)


class DateRangeParams(BaseModel, DateRangeFilter):
    pass


class PaginationParams(BaseModel, PaginationFilter):
    pass
