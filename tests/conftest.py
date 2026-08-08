import pytest

from app.config import settings


@pytest.fixture(scope="session", autouse=True)
def verify_test_db():
    if not settings.postgres_db.endswith("_test"):
        pytest.exit(f"Not a test db: '{settings.postgres_db}'", returncode=1)
