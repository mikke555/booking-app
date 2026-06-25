from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base


class BaseRepository[ModelT: Base, SchemaT: BaseModel]:
    model: type[ModelT]
    schema: type[SchemaT]

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_schema(self, entity: ModelT) -> SchemaT:
        return self.schema.model_validate(entity)

    async def get_by_id(self, id: int) -> SchemaT | None:
        entity = await self.session.get(self.model, id)
        if entity is None:
            return None
        return self._to_schema(entity)

    async def list(
        self, *filters, limit: int = 10, offset: int = 0, **filter_by
    ) -> list[SchemaT]:
        stmt = select(self.model)

        if filter_by:
            stmt = stmt.filter_by(**filter_by)

        if filters:
            stmt = stmt.where(*filters)

        stmt = stmt.order_by(self.model.id).limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return [self._to_schema(row) for row in result.scalars().all()]

    async def add(self, data: BaseModel) -> SchemaT:
        entity = self.model(**data.model_dump())
        self.session.add(entity)
        await self.session.flush()
        return self._to_schema(entity)

    async def update(self, id: int, data: BaseModel) -> SchemaT | None:
        entity = await self.session.get(self.model, id)
        if entity is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(entity, key, value)
        await self.session.flush()
        return self._to_schema(entity)

    async def delete(self, id: int) -> bool:
        entity = await self.session.get(self.model, id)
        if entity is None:
            return False
        await self.session.delete(entity)
        return True
