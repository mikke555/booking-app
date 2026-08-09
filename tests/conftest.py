from datetime import date

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

import app.models  # noqa: F401
from app.config import settings
from app.database import Base, engine
from app.dependencies import get_db_manager
from app.main import app
from app.utils.db_manager import DBManager
from app.utils.security import create_access_token
from tests.const import DATE_FROM, DATE_TO

PASSWORD = "password123"
PASSWORD_HASH = "$argon2id$v=19$m=65536,t=3,p=4$5EA2LBGgz4ZnUJav8JcmeA$RyOCu4XpSCph+/TGxhsw54t1/d3fTvjVtHrorbSRDmU"


@pytest.fixture(scope="session", autouse=True)
def guard():
    if not settings.postgres_db.endswith("_test"):
        pytest.exit(f"Not a test db: '{settings.postgres_db}'", returncode=1)


# Once per run: fresh db schema
# Once per test: outer transaction w/ rollback + dep override


@pytest.fixture(scope="session")
async def setup_db(guard):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


@pytest.fixture(autouse=True)
async def db_transaction(setup_db):
    async with engine.connect() as conn:
        trans = await conn.begin()

        yield async_sessionmaker(
            bind=conn,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        await trans.rollback()


@pytest.fixture(autouse=True)
async def override_db(db_transaction):
    async def override_get_db_manager():
        async with DBManager(db_transaction) as db:
            yield db

    app.dependency_overrides[get_db_manager] = override_get_db_manager
    yield

    app.dependency_overrides.clear()


# Test-facing fixtures


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def db(db_transaction):
    async with DBManager(db_transaction) as db:
        yield db


# Users & auth


@pytest.fixture
async def user(db):
    user = await db.users.add(email="user@example.com", hashed_password=PASSWORD_HASH)
    await db.commit()
    return user


@pytest.fixture
async def admin(db):
    admin = await db.users.add(
        email="admin@example.com", hashed_password=PASSWORD_HASH, is_admin=True
    )
    await db.commit()
    return admin


@pytest.fixture
def user_headers(user):
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


@pytest.fixture
def admin_headers(admin):
    return {"Authorization": f"Bearer {create_access_token(admin.id)}"}


# Hotels, rooms & bookings


@pytest.fixture
async def hotel(db):
    hotel = await db.hotels.add(name="Affordable Palace", location="Château d'Or")
    await db.commit()
    return hotel


@pytest.fixture
async def room(db, hotel):
    room = await db.rooms.add(
        hotel_id=hotel.id,
        title="Standard",
        description="Room with a view of the parking lot",
        price=100,
        quantity=2,
    )
    await db.commit()
    return room


@pytest.fixture
async def amenity(db):
    amenity = await db.amenities.add(name="Wi-Fi")
    await db.commit()
    return amenity


@pytest.fixture
def make_booking(db, user):
    async def _make_booking(room):
        booking = await db.bookings.add(
            room_id=room.id,
            user_id=user.id,
            date_from=date.fromisoformat(DATE_FROM),
            date_to=date.fromisoformat(DATE_TO),
            price=room.price,
        )
        await db.commit()
        return booking

    return _make_booking
