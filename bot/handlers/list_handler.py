from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from crud.activities import activity_crud

router = Router()


@router.message(F.text == '/list')
async def get_list_of_activities(message: Message, session: AsyncSession):

    activities = await activity_crud.get_activities_list_by_telegram_id(
        telegram_id=message.from_user.id,
        session=session
    )

    activities_str = ''

    for activity in reversed(activities):
        activities_str = activities_str + str(activity) + '\n'

    await message.answer(text=activities_str)
