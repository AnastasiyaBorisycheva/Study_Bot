from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import confirm_keyboard, get_activities_list_keyboard
from crud.activities import activity_crud

router = Router()


class DeleteState(StatesGroup):
    waiting_confirmation = State()
    confirmation_yes = State()
    confirmation_no = State()


@router.message(F.text == '/delete')
async def get_list_of_activities(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    await message.answer(
        'Список активностей:',
        reply_markup=await get_activities_list_keyboard(
            session=session,
            telegram_id=message.from_user.id,
            callback_text='delete_activity',
            router=router
            )
        )


@router.callback_query(F.data.startswith('delete_activity:'))
async def get_users_activity(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):

    activity_id = int(callback.data.removeprefix('delete_activity:'))
    activity = await activity_crud.get(
        id=activity_id,
        session=session
    )

    await callback.message.edit_text(
        text=(
            f'Удалить запись об активности?\n'
            f'{activity}'
        ),
        reply_markup=confirm_keyboard()
    )

    await callback.answer()

    await state.set_state(DeleteState.waiting_confirmation)
    await state.update_data(telegram_id=callback.from_user.id)
    await state.update_data(activity_id=activity_id)


@router.callback_query(
    F.data.startswith('confirm_'),
    DeleteState.waiting_confirmation
)
async def delete_users_activity(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):

    if callback.data == 'confirm_yes':
        await activity_crud.delete(
            session=session,
            id=await state.get_value('activity_id')
        )

        await callback.message.edit_text(
            text='Запись удалена',
            reply_markup=None
        )

    elif callback.data == 'confirm_no':
        await callback.message.edit_text(
            text='Операция отменена',
            reply_markup=None
        )

    await callback.answer()
    await state.clear()
