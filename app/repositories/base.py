from typing import Any

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base


class BaseRepository[ModelT: Base, SchemaT: BaseModel]:
    model: type[ModelT]
    schema: type[SchemaT]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> SchemaT | None:
        object = await self.session.get(self.model, id)
        if object is None:
            return None
        return self.schema.model_validate(object)

    async def list(
        self, limit: int = 10, offset: int = 0, **filter_by: Any
    ) -> list[SchemaT]:
        stmt = select(self.model).filter_by(**filter_by).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return [self.schema.model_validate(object) for object in result.scalars().all()]

    async def add(self, data: BaseModel) -> SchemaT:
        object = self.model(**data.model_dump())
        self.session.add(object)
        await self.session.flush()
        return self.schema.model_validate(object)

    async def update(self, id: int, data: BaseModel) -> SchemaT | None:
        object = await self.session.get(self.model, id)
        if object is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(object, key, value)
        await self.session.flush()
        return self.schema.model_validate(object)

    async def delete(self, id: int) -> bool:
        object = await self.session.get(self.model, id)
        if object is None:
            return False
        await self.session.delete(object)
        return True
