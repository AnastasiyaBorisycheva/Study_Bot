from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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


def type_of_date_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Утро", callback_data="morning")],
            [InlineKeyboardButton(text="День", callback_data="day")],
            [InlineKeyboardButton(text="Вечер", callback_data="evening")],
            [InlineKeyboardButton(text="Ночь", callback_data="night")],
            [InlineKeyboardButton(text="Весь день", callback_data="all_day")]
        ]
    )
