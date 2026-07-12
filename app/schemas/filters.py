from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field, model_validator


class DateRangeParams(BaseModel):
    date_from: Annotated[date, Field(json_schema_extra={"example": "2026-07-12"})]
    date_to: Annotated[date, Field(json_schema_extra={"example": "2026-07-15"})]

    @model_validator(mode="after")
    def check_dates(self) -> DateRangeParams:
        if self.date_from >= self.date_to:
            raise ValueError("date_from must be earlier than date_to")
        return self
