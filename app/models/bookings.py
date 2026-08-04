from datetime import date, datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    __table_args__ = (
        CheckConstraint(
            "date_to > date_from",
            name="ck_bookings_valid_dates",
        ),
        CheckConstraint(
            "price >= 0",
            name="ck_bookings_price_non_negative",
        ),
        Index("ix_bookings_room_dates", "room_id", "date_from", "date_to"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    @property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days
