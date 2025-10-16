from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import (activity_subtypes_keyboard, activity_types_keyboard,
                           duration_keyboard, type_of_date_inline_keyboard)
from crud.activities import activity_crud
from crud.activity_subtypes import activity_subtype_crud


class ActivityState(StatesGroup):
    waiting_date = State()
    waiting_duration = State()
    waiting_daypart = State()
    waiting_activity_type = State()
    waiting_activity_sybtype = State()


router = Router()


@router.message(F.text == '/add')
async def StartAddActivity(message: Message, state: FSMContext):

    calendar = SimpleCalendar(show_alerts=True)

    msg_year = message.date.year
    msg_month = message.date.month

    calendar.set_dates_range(
            min_date=(datetime.now() - timedelta(days=90)),
            max_date=datetime.now()
        )

    await message.answer(
        "Выберите дату для записи",
        reply_markup=await calendar.start_calendar(
            year=msg_year,
            month=msg_month
        )
    )

    await state.set_state(ActivityState.waiting_date)
    await state.update_data(telegram_id=message.from_user.id)


@router.callback_query(
        SimpleCalendarCallback.filter(),
        ActivityState.waiting_date
    )
async def process_calendar(
    callback: CallbackQuery,
    callback_data: SimpleCalendarCallback,
    state: FSMContext
):
    calendar = SimpleCalendar(show_alerts=True)
    calendar.set_dates_range(
            min_date=(datetime.now() - timedelta(days=90)),
            max_date=datetime.now()
        )

    selected, input_date = await calendar.process_selection(
        callback,
        callback_data
    )

    if selected:
        await callback.message.edit_text(
            f"✅ Формируем запись на дату: {input_date.strftime('%d.%m.%Y')}",
            reply_markup=None
        )

        await state.update_data(activity_date=input_date)
        await state.set_state(ActivityState.waiting_duration)
        await callback.answer()

        await callback.message.answer(
            "Введите продолжительность действия",
            reply_markup=duration_keyboard()
        )


@router.message(ActivityState.waiting_duration)
async def process_duration(message: Message, state: FSMContext):

    try:
        input_number = int(message.text)
        if input_number <= 0:
            await message.answer('Продолжительность должна быть больше 0')
            return
        elif input_number >= 600:
            await message.answer('Не может быть!')
            return

        msg = await message.answer('+', reply_markup=ReplyKeyboardRemove())
        await msg.delete()

        await state.update_data(duration=input_number)
        await state.set_state(ActivityState.waiting_daypart)

        await message.answer(
            "Выберите часть дня",
            reply_markup=type_of_date_inline_keyboard()
        )

    except Exception as e:
        print(e)
        await message.answer("Продолжительность должна быть числом")
        return


@router.callback_query(
        ActivityState.waiting_daypart,
        F.data.startswith('daypart:')
    )
async def process_daypart(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):

    keyboard = callback.message.reply_markup.inline_keyboard

    for row in keyboard:
        for button in row:
            if button.callback_data == callback.data:
                button_text = button.text
                break

    await state.update_data(daypart=button_text)
    await state.set_state(ActivityState.waiting_activity_type)

    await callback.message.edit_text(
       "Выберите вид активности",
       reply_markup=await activity_types_keyboard(session=session)
    )
    await callback.answer()


@router.callback_query(
        ActivityState.waiting_activity_type,
        F.data.startswith("activity_type:")
    )
async def process_activity_type(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):

    activity_type_id = callback.data.split(':')[-1]

    await state.set_state(ActivityState.waiting_activity_sybtype)

    await callback.message.edit_text(
        "Выберите тип активности",
        reply_markup=await activity_subtypes_keyboard(
            session,
            int(activity_type_id)
        )
    )
    await callback.answer()


@router.callback_query(
        ActivityState.waiting_activity_sybtype,
        F.data.startswith("activity_subtype:")
    )
async def process_activity_add(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):

    activity_subtype_id = callback.data.split(':')[-1]
    activity_subtype_obj = await activity_subtype_crud.get(
        int(activity_subtype_id),
        session
    )

    await state.update_data(activity_subtype=activity_subtype_obj)
    data = await state.get_data()

    await activity_crud.create(session, data)

    await callback.message.edit_text("Данные добавлены", reply_markup=None)
    await callback.answer()

    await state.clear()
