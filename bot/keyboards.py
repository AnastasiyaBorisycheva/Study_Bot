from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from crud.activity_subtypes import activity_subtype_crud
from crud.activity_types import activity_type_crud


# Клавиатура для подтверждения
def confirm_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data="confirm_yes")],
        [InlineKeyboardButton(text="❌ Нет", callback_data="confirm_no")]
    ])


def duration_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='30'), KeyboardButton(text='60')],
            [KeyboardButton(text='90'), KeyboardButton(text='120')],
            [KeyboardButton(text='180'), KeyboardButton(text='210')],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def type_of_date_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Утро", callback_data="daypart:morning")],
            [InlineKeyboardButton(text="День", callback_data="daypart:day")],
            [InlineKeyboardButton(text="Вечер", callback_data="daypart:evening")],
            [InlineKeyboardButton(text="Ночь", callback_data="daypart:night")],
            [InlineKeyboardButton(text="Весь день", callback_data="daypart:all_day")]
        ]
    )


async def activity_types_keyboard(session: AsyncSession):
    activity_types = await activity_type_crud.get_all(session=session)

    builder = InlineKeyboardBuilder()

    for activity_type in activity_types:
        builder.button(
            text=activity_type.activity_type_name,
            callback_data=f'activity_type:{activity_type.id}'
        )

    builder.adjust(2)

    return builder.as_markup()


async def activity_subtypes_keyboard(session: AsyncSession, activity_type_id: int):
    activity_sybtypes = await activity_subtype_crud.get_subtypes_by_activite(
        session=session,
        activity_type_id=activity_type_id
    )

    builder = InlineKeyboardBuilder()

    for activity_subtype in activity_sybtypes:
        builder.button(
            text=activity_subtype.activity_subtype_name,
            callback_data=f'activity_subtype:{activity_subtype.id}'
        )

    builder.adjust(2)

    return builder.as_markup()
