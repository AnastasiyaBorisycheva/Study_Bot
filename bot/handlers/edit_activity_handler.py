from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import (activity_subtypes_keyboard, activity_types_keyboard,
                           duration_keyboard,
                           edit_confirmation_inline_keyboard,
                           get_activities_list_keyboard,
                           show_activity_parameters_keyboard,
                           type_of_date_inline_keyboard)
from crud.activities import activity_crud
from crud.activity_subtypes import activity_subtype_crud

router = Router()


class EditState(StatesGroup):
    waiting_activity = State()
    waiting_parameter = State()

    edit_activity_date = State()
    edit_duration = State()
    edit_daypart = State()
    edit_activity_type = State()
    edit_activity_subtype = State()

    waiting_confirmation = State()


@router.message(F.text == '/edit')
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
            callback_text='edit_activity',
            router=router
            )
        )

    await state.set_state(EditState.waiting_activity)


@router.callback_query(
    or_f(
        F.data.startswith('edit_activity:'),
        EditState.waiting_activity
    )
)
async def eidt_activity_list_options(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    activity_id = int(callback.data.removeprefix('edit_activity:'))
    activity = await activity_crud.get(activity_id, session)

    await callback.message.edit_text(
        text=(
            f'Выбрана активность {activity}\n'
            f'Что хотите изменить?'
        ),
        reply_markup=show_activity_parameters_keyboard()
    )

    await state.update_data(activity=activity)
    await state.update_data(activity_id=activity_id)
    await state.set_state(EditState.waiting_parameter)
    await callback.answer()


@router.callback_query(
    F.data.startswith('edit_param:'),
    EditState.waiting_parameter
)
async def choose_edit_param(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):

    parameter = callback.data.removeprefix('edit_param:')
    parameter_state = 'edit_' + parameter

    print(f"Выбран параметр: {parameter}")

    activity = await state.get_value('activity')

    if parameter == 'activity_date':
        calendar = SimpleCalendar(show_alerts=True)

        msg_year = message.date.year
        msg_month = message.date.month

        calendar.set_dates_range(
                min_date=(datetime.now() - timedelta(days=90)),
                max_date=datetime.now()
            )

        await callback.message.edit_text(
            text=(
                f'Текущая дата: {activity.formatted_date}\n'
                f'Выберите новую дату'
            ),
            reply_markup=await calendar.start_calendar(
                year=msg_year,
                month=msg_month
            )
        )

    elif parameter == 'duration':
        await callback.message.answer(
            text=(
                f'Текущая продолжительность: {activity.duration}\n'
                f'Введите новую продолжительность действия'
            ),
            reply_markup=duration_keyboard()
        )

    elif parameter == 'daypart':
        await callback.message.edit_text(
            text=(
                f'Текущая часть дня: {activity.daypart}\n'
                f'Выберите новую часть дня'
            ),
            reply_markup=type_of_date_inline_keyboard()
        )

    elif parameter == 'activity_type':
        await callback.message.edit_text(
            text=(
                f'Текущий вид активности:'
                f'{activity.activity_subtype.activity_type.activity_type_name}'
                f'\n'
                f'Выберите новый вид активности'
            ),
            reply_markup=await activity_types_keyboard(session=session)
        )

    else:
        print('Неизвестный параметр')

    try:
        state_to_set = getattr(EditState, parameter_state)
        await state.set_state(state_to_set)
        current_state = await state.get_state()
        print(f"Текущее состояние: {current_state}")
    except AttributeError:
        print(f"Состояние {parameter} не существует в классе EditState")

    await callback.answer()


@router.callback_query(
    SimpleCalendarCallback.filter(),
    EditState.edit_activity_date
)
async def edit_activity_date(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: SimpleCalendarCallback,
    session: AsyncSession
):

    print("Попали в обработчик даты!")  # ← отладка
    current_state = await state.get_state()
    print(f"Состояние в обработчике: {current_state}")

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
            text=(
                f"Новая дата: {input_date.strftime('%d.%m.%Y')}"
            ),
            reply_markup=None
        )

        await state.update_data(activity_date=input_date)

        await callback.message.answer(
            text='Хотите изменить что-то еще?',
            reply_markup=edit_confirmation_inline_keyboard()
        )

        await state.set_state(EditState.waiting_confirmation)

    await callback.answer()


@router.message(EditState.edit_duration)
async def edit_duration(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    try:
        input_number = int(message.text)
        if input_number <= 0:
            await message.answer('Продолжительность должна быть больше 0')
            return
        elif input_number >= 600:
            await message.answer('Не может быть!')
            return

        await state.update_data(duration=input_number)
        await message.answer(
            f'Новая продолжительность {input_number} мин.',
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            text='Хотите изменить что-то еще?',
            reply_markup=edit_confirmation_inline_keyboard()
        )
        await state.set_state(EditState.waiting_confirmation)

    except Exception as e:
        print(e)
        await message.answer("Продолжительность должна быть числом")
        return


@router.callback_query(
    EditState.edit_daypart
)
async def edit_activity_daypart(
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

    await callback.message.edit_text(
        text=f'Новая часть дня: {button_text}',
        reply_markup=None
    )

    await callback.message.answer(
        text='Хотите изменить что-то еще?',
        reply_markup=edit_confirmation_inline_keyboard()
    )

    await state.update_data(daypart=button_text)
    await state.set_state(EditState.waiting_confirmation)
    await callback.answer()


@router.callback_query(
    EditState.edit_activity_type
)
async def edit_activity_type(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    activity_type_id = callback.data.split(':')[-1]
    await callback.message.edit_text(
        "Выберите тип активности",
        reply_markup=await activity_subtypes_keyboard(
            session,
            int(activity_type_id)
        )
    )

    await state.update_data(activity_type_id=int(activity_type_id))
    await state.set_state(EditState.edit_activity_subtype)
    await callback.answer()


@router.callback_query(
    EditState.edit_activity_subtype
)
async def edit_activity_subtype(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):

    activity_subtype_id = callback.data.split(':')[-1]
    activity_subtype_obj = await activity_subtype_crud.get(
        int(activity_subtype_id),
        session
    )

    await state.update_data(activity_subtype_id=int(activity_subtype_id))
    # await state.update_data(activity_subtype=activity_subtype_obj)
    await state.set_state(EditState.waiting_confirmation)

    await callback.message.edit_text(
        text=f'Новый вид активности\n {activity_subtype_obj}'
    )

    await callback.message.answer(
        text='Хотите изменить что-то еще?',
        reply_markup=edit_confirmation_inline_keyboard()
    )
    await callback.answer()


@router.callback_query(
    EditState.waiting_confirmation
)
async def edit_confirmation(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):

    print('Обрабатываем подтверждение')
    print(await state.get_data())

    activity_id = await state.get_value('activity_id')
    activity = await activity_crud.get(activity_id, session)

    if callback.data.endswith('save'):
        new_activity = await activity_crud.update(
            session=session,
            id=activity_id,
            data=await state.get_data()
        )

        await callback.message.edit_text(
            text=(
                f'Данные обновлены\n'
                f'{new_activity}'
            )
        )

        await state.clear()

    elif callback.data.endswith('continue'):

        await callback.message.edit_text(
            text=(
                f'Текущая активность: {activity}\n'
                f'Данные не обновлены\n'
                f'Хотите изменить что-то еще?'
            ),
            reply_markup=show_activity_parameters_keyboard()
        )

        await state.set_state(EditState.waiting_parameter)

    await callback.answer()
