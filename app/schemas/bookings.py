from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, model_validator


class BookingBase(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingRead(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BookingBase):
    @model_validator(mode="after")
    def check_dates(self) -> BookingCreate:
        if self.date_from < date.today():
            raise ValueError("date_from cannot be in the past")
        if self.date_from >= self.date_to:
            raise ValueError("date_from must be earlier than date_to")
        return self
