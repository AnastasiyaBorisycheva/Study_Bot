from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_widgets.pagination import KeyboardPaginator
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router

from crud.activity_subtypes import activity_subtype_crud
from crud.activity_types import activity_type_crud
from crud.activities import activity_crud


# Клавиатура для подтверждения
def confirm_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data="confirm_yes")],
        [InlineKeyboardButton(text="❌ Нет", callback_data="confirm_no")]
    ])


def delete_or_edit_keyboard(
    activity_id: int
):
    keyboard = [
        [
            InlineKeyboardButton(
                text="Редактировать",
                callback_data=f"edit_activity:{activity_id}"
            ),
            InlineKeyboardButton(
                text="Удалить",
                callback_data=f"delete_activity:{activity_id}"
            ),
        ]
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def duration_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='30'), KeyboardButton(text='60'), KeyboardButton(text='90')],
            [KeyboardButton(text='120'), KeyboardButton(text='150'), KeyboardButton(text='180')],
            [KeyboardButton(text='210'), KeyboardButton(text='240'), KeyboardButton(text='270')],
            [KeyboardButton(text='300'), KeyboardButton(text='330'), KeyboardButton(text='360')],
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


async def activity_subtypes_keyboard(
    session: AsyncSession,
    activity_type_id: int
):
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


async def get_activities_list_keyboard(
        session: AsyncSession,
        telegram_id: int,
        callback_text: str,
        router: Router
):

    activities = await activity_crud.get_activities_list_by_telegram_id(
        telegram_id=telegram_id,
        session=session
    )

    buttons = []

    for activity in activities:
        button = InlineKeyboardButton(
            text=(
                f"{activity.formatted_date}: "
                f"{activity.activity_subtype.activity_type.activity_type_name} - "
                f"{activity.activity_subtype.activity_subtype_name}, "
                f"{activity.duration} мин."
            ),
            callback_data=f'{callback_text}:{activity.id}'
        )

        buttons.append(button)

    paginator = KeyboardPaginator(
        data=buttons,
        router=router,
        per_page=10,
        per_row=1
    )

    return paginator.as_markup()
