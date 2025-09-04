from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import crud_user

router = Router()



@router.message(CommandStart())
async def command_start_handler(
        message: Message,
        session: AsyncSession, 
        state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """

    telegram_user_id = message.from_user.id

    await state.clear()

    user_info = await crud_user.get_by_telegram_id(telegram_user_id, session)

    if not user_info:
        data = {}
        data['telegram_id'] = telegram_user_id
        data['first_name'] = message.from_user.first_name
        data['last_name'] = message.from_user.last_name
        data['username'] = message.from_user.username
        data['is_premium'] = message.from_user.is_premium

        await crud_user.create(session, data=data)
        await message.answer(
            f"User {message.from_user.username} has been registrated"
        )
    else:
        await message.answer(
            f"Hello, {message.from_user.username}!"
        )
