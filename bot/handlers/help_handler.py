from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession


router = Router()


@router.message(F.text == '/help')
async def command_help(
    message: Message
):

    message_text = (
        f'Начни с команды start \n'
        f'Для добавления активности используй add \n'
        f'Посмотри список своей активности через list \n'
        f'Если ничего непонятно, пиши мне @Anastasiia_Mist'
    )

    await message.answer(text=message_text)