from aiogram import BaseMiddleware, types
from typing import Callable, Awaitable, Any, Dict
from database.engine import AsyncSessionLocal


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ) -> Any:
        async with AsyncSessionLocal() as session:
            data["session"] = session  # Добавляем сессию в data
            return await handler(event, data)
