from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from crud.activity_subtypes import activity_subtype_crud
from crud.activity_types import activity_type_crud


# Клавиатура для выбора пола
def gender_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨 Мужской", callback_data="gender_m")],
        [InlineKeyboardButton(text="👩 Женский", callback_data="gender_f")]
    ])


# Клавиатура для подтверждения
def confirm_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data="confirm_yes")],
        [InlineKeyboardButton(text="❌ Нет", callback_data="confirm_no")]
    ])


def type_of_date_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Утро", callback_data="morning")],
            [InlineKeyboardButton(text="День", callback_data="day")],
            [InlineKeyboardButton(text="Вечер", callback_data="evening")],
            [InlineKeyboardButton(text="Ночь", callback_data="night")],
            [InlineKeyboardButton(text="Весь день", callback_data="all_day")]
        ]
    )


def type_of_date_button_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Утро")],
            [KeyboardButton(text="День")],
            [KeyboardButton(text="Вечер")],
            [KeyboardButton(text="Ночь")],
            [KeyboardButton(text="Весь день")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def test_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='First_button', )],
            [KeyboardButton(text='Second_button'), KeyboardButton(text='Third_button')],

        ],
        is_persistent=False,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='test_button',
        selective=True
    )


async def activity_types_keyboard(session: AsyncSession):
    activity_types = await activity_type_crud.get_all(session=session)

    buttons = []

    for activity_type in activity_types:
        buttons.append(KeyboardButton(text=activity_type.activity_type_name))

    keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[
            buttons
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard_markup


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
