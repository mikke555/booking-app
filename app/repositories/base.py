from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base


class BaseRepository[ModelT: Base]:
    model: type[ModelT]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int, *, for_update: bool = False) -> ModelT | None:
        return await self.session.get(
            self.model, id, with_for_update=for_update or None
        )

    async def get_one_by_filter(self, **filter_by) -> ModelT | None:
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self, *filters, limit: int | None = None, offset: int | None = None, **filter_by
    ) -> list[ModelT]:
        stmt = select(self.model)

        if filter_by:
            stmt = stmt.filter_by(**filter_by)
        if filters:
            stmt = stmt.where(*filters)

        stmt = stmt.order_by(self.model.id)

        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add(self, **values) -> ModelT:
        entity = self.model(**values)
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def update(self, entity: ModelT, values: dict) -> ModelT:
        for key, value in values.items():
            setattr(entity, key, value)
        await self.session.flush()
        return entity

    async def delete(self, entity: ModelT) -> None:
        await self.session.delete(entity)
