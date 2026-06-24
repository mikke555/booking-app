from typing import AsyncGenerator

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
from typing import Annotated


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.database_url, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession | None]:
    async with SessionLocal() as session:
        yield session


sessionDep = Annotated[AsyncSession, Depends(get_session)]
