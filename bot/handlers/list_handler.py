from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import delete_or_edit_keyboard, get_activities_list_keyboard
from crud.activities import activity_crud

router = Router()


@router.message(F.text == '/list')
async def get_list_of_activities(message: Message, session: AsyncSession):

    await message.answer(
        'Список активностей:',
        reply_markup=await get_activities_list_keyboard(
            session=session,
            telegram_id=message.from_user.id,
            callback_text='users_activity',
            router=router
            )
        )


@router.callback_query(F.data.startswith('users_activity:'))
async def show_edit_or_delete_question(
    callback: CallbackQuery,
    session: AsyncSession
):

    activity_id = int(callback.data.removeprefix('users_activity:'))

    activity = await activity_crud.get(
        id=activity_id,
        session=session
    )

    await callback.message.edit_text(
        text=f'Активность {activity}',
        reply_markup=delete_or_edit_keyboard(activity_id)
    )

    await callback.answer()
