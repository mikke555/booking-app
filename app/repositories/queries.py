from datetime import date
from typing import Any

from sqlalchemy import Select, func, select

from app.models.bookings import Booking
from app.models.rooms import Room


def available_rooms_stmt(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
) -> Select[Any]:
    booked_count = func.count(Booking.id)

    stmt = (
        select(Room, (Room.quantity - booked_count).label("quantity_left"))
        .outerjoin(
            Booking,
            (Booking.room_id == Room.id)
            & (Booking.date_from < date_to)
            & (Booking.date_to > date_from),
        )
        .group_by(Room.id)
        .having(Room.quantity > booked_count)
    )

    if hotel_id is not None:
        stmt = stmt.filter(Room.hotel_id == hotel_id)

    return stmt


def available_hotel_ids_stmt(date_from: date, date_to: date) -> Select[Any]:
    return available_rooms_stmt(date_from, date_to).with_only_columns(Room.hotel_id)
