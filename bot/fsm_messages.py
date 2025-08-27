from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram import Router, html, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import type_of_date_keyboard


class Registration(StatesGroup):
    wait_name = State()        # Ждем имя
    wait_age = State()         # Ждем возраст
    wait_photo = State()       # Ждем фото
    confirmation = State()     # Подтверждение данных



router = Router()


@router.callback_query(F.data == "cancel")
async def cancel_survey(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Опрос отменен")
    await callback.answer()



@router.message(CommandStart())
async def command_start_handler(
        message: Message,
        session: AsyncSession) -> None:
    """
    This handler receives messages with `/start` command
    """

    await message.answer("Hello", reply_markup=type_of_date_keyboard())
