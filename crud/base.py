from typing import Type, TypeVar, Generic, Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(self, id: int, session: AsyncSession,):
        """Получить объект по ID."""
        result = await session.execute(
            select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(
            self,
            session: AsyncSession,
            skip: int = 0,
            limit: int = 10,
    ):
        """Получить все объекты с пагинацией."""
        result = await session.execute(
            select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, session: AsyncSession, data: Dict[str, Any]):
        """Создать новый объект."""

        obj = self.model(**data)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def update(self, session: AsyncSession, id: int, data: Dict[str, Any]):
        """Обновить объект."""
        await session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
        )
        await session.commit()
        return await self.get(id)

    async def delete(self, session: AsyncSession, id: int) -> bool:
        """Удалить объект."""
        await session.execute(
            delete(self.model).where(self.model.id == id))
        await session.commit()
        return True

    async def get_by_attribute(
            self,
            attr_name: str,
            attr_value: str,
            session: AsyncSession,
    ):
        """Получить объект по значению атрибута."""
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()
