from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery


router = Router()


@router.message(F.text == '/cancel')
async def cansel_survey(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Диалог отменен", reply_markup=ReplyKeyboardRemove())


@router.callback_query(F.data == '/cancel')
async def cansel_survey_inline(
    callback: CallbackQuery,
    state: FSMContext,
):

    await state.clear()
    await callback.message.edit_text(
        text="Диалог отменен",
        reply_markup=None
    )
    await callback.answer(text='Диалог отменен')
