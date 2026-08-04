"""Seed the empty database with demo data.

Usage: uv run python -m scripts.seed
"""

import asyncio
import sys
from datetime import timedelta

from sqlalchemy import func, select

from app.database import session_factory
from app.models.hotels import Hotel
from app.models.users import User
from app.utils.clock import today
from app.utils.db_manager import DBManager
from app.utils.security import hash_password

ADMIN_EMAIL = "admin@booking.app"
PASSWORD = "password123"

current_date = today()


async def seed(db: DBManager) -> list[User]:
    wifi = await db.amenities.add(name="Wi-Fi")
    tv = await db.amenities.add(name="TV")
    ac = await db.amenities.add(name="Air conditioning")
    minibar = await db.amenities.add(name="Mini bar")
    sea_view = await db.amenities.add(name="Sea view")
    breakfast = await db.amenities.add(name="Breakfast included")

    anchor = await db.hotels.add(name="The Rusty Anchor Inn", location="Portsmouth")
    lodge = await db.hotels.add(name="Northern Lights Lodge", location="Tromsø")
    cactus = await db.hotels.add(name="The Sleepy Cactus", location="Tucson")
    alpinist = await db.hotels.add(
        name="Dead Mountaineer's Hotel", location="Bottleneck Pass"
    )

    single = await db.rooms.add(
        hotel_id=anchor.id,
        title="Deckhand Single",
        description="Compact room with a single bunk and porthole window",
        quantity=5,
        price=90,
        amenities=[wifi, tv],
    )
    double = await db.rooms.add(
        hotel_id=anchor.id,
        title="Harbour View Double",
        description="Room with a double bed overlooking the marina",
        quantity=3,
        price=150,
        amenities=[wifi, tv, sea_view],
    )
    await db.rooms.add(
        hotel_id=lodge.id,
        title="Standard Twin",
        description="Cosy twin room with a fireplace",
        quantity=4,
        price=200,
        amenities=[wifi, tv, ac, minibar],
    )
    suite = await db.rooms.add(
        hotel_id=lodge.id,
        title="Aurora Panorama Suite",
        description="Suite with a glass ceiling for northern lights viewing",
        quantity=2,
        price=350,
        amenities=[wifi, tv, ac, minibar, breakfast],
    )
    await db.rooms.add(
        hotel_id=cactus.id,
        title="Stargazer Bungalow",
        description="Desert bungalow with a rooftop stargazing deck",
        quantity=6,
        price=180,
        amenities=[wifi, tv, ac],
    )
    await db.rooms.add(
        hotel_id=alpinist.id,
        title="Room-with-Fireplace",
        description="Snug room upstairs; the previous guest never checked out",
        quantity=3,
        price=120,
        amenities=[wifi, minibar],
    )
    await db.rooms.add(
        hotel_id=alpinist.id,
        title="Museum Suite",
        description="Suite preserved exactly as the mountaineer left it",
        quantity=1,
        price=280,
        amenities=[wifi, tv, minibar, breakfast],
    )

    admin = await db.users.add(
        email=ADMIN_EMAIL, hashed_password=hash_password(PASSWORD), is_admin=True
    )
    alice = await db.users.add(
        email="alice@example.com", hashed_password=hash_password(PASSWORD)
    )
    bob = await db.users.add(
        email="bob@example.com", hashed_password=hash_password(PASSWORD)
    )

    await db.bookings.add(
        room_id=single.id,
        user_id=alice.id,
        date_from=current_date + timedelta(days=7),
        date_to=current_date + timedelta(days=10),
        price=single.price,
    )
    await db.bookings.add(
        room_id=double.id,
        user_id=alice.id,
        date_from=current_date + timedelta(days=30),
        date_to=current_date + timedelta(days=33),
        price=double.price,
    )
    await db.bookings.add(
        room_id=suite.id,
        user_id=bob.id,
        date_from=current_date + timedelta(days=14),
        date_to=current_date + timedelta(days=21),
        price=suite.price,
    )

    return [admin, alice, bob]


async def main() -> None:
    async with DBManager(session_factory) as db:
        if await db.session.scalar(select(func.count(Hotel.id))):
            sys.exit("Database is not empty - refusing to seed.")

        users = await seed(db)
        await db.commit()

    print("Seeded users:")
    for user in users:
        print(f"  {user.email:<24}{PASSWORD}")


if __name__ == "__main__":
    asyncio.run(main())
