import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

import app.models  # noqa: F401
from app.config import settings
from app.database import Base, engine
from app.dependencies import get_db_manager
from app.main import app
from app.utils.db_manager import DBManager


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
