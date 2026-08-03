from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.amenities import Amenity


class Room(Base):
    __tablename__ = "rooms"

    __table_args__ = (
        CheckConstraint("quantity >= 1", name="ck_rooms_quantity_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    hotel_id: Mapped[int] = mapped_column(
        ForeignKey("hotels.id", ondelete="CASCADE"), index=True
    )

    amenities: Mapped[list[Amenity]] = relationship(
        secondary="room_amenities", back_populates="rooms"
    )
