from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import get_activities_list_keyboard

router = Router()


@router.message(F.text == '/list')
async def get_list_of_activities(message: Message, session: AsyncSession):

    await message.answer(
        'Список активностей:',
        reply_markup=await get_activities_list_keyboard(
            session=session,
            telegram_id=message.from_user.id,
            router=router
            )
        )
