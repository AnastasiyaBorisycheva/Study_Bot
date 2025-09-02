from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from database.models import User


class UserCRUD(CRUDBase):
    def __init__(self):
        super().__init__(User)

    async def get_by_telegram_id(self, telegram_id: int, session: AsyncSession) -> Optional[User]:
        """Найти пользователя по telegram_id."""
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    async def create_or_update(self, telegram_id: int, session: AsyncSession, **kwargs) -> User:
        """Создать или обновить пользователя."""
        user = await self.get_by_telegram_id(telegram_id=telegram_id, session=session)
        if user:
            await self.update(session, user.id, **kwargs)
        else:
            user = await self.create(session=session, data={"telegram_id": telegram_id, **kwargs})
        return user


crud_user = UserCRUD()
