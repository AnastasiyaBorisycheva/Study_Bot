from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from bot.keyboards import activity_types_keyboard, type_of_date_button_keyboard, activity_subtypes_keyboard

from crud.activities import activity_crud
from crud.activity_types import activity_type_crud
from crud.activity_subtypes import activity_subtype_crud


class ActivityState(StatesGroup):
    waiting_date = State()
    waiting_duration = State()
    waiting_daypart = State()
    waiting_activity_type = State()
    waiting_activity_sybtype = State()
    confirmation = State()     # Подтверждение данных


router = Router()


@router.message(F.text == '/add')
async def StartAddActivity(message: Message, state: FSMContext):
    await message.answer("Введите дату в формате дд.мм.гггг")
    await state.set_state(ActivityState.waiting_date)
    await state.update_data(telegram_id=message.from_user.id)


@router.message(ActivityState.waiting_date)
async def process_date(message: Message, state: FSMContext):

    input_date = message.text
    try:
        input_datetime = datetime.strptime(input_date, "%d.%m.%Y")

        if input_datetime > datetime.today():
            await message.answer("Дата не должна быть будущим числом")
            await message.answer("Введите дату в формате дд.мм.гггг")
            return
        else:
            await message.answer("Введите продолжительность действия")
            await state.update_data(activity_date=input_datetime)
            await state.set_state(ActivityState.waiting_duration)

    except Exception as e:
        print(e)
        await message.answer("Ведите дату в формате дд.мм.гггг")
        return


@router.message(ActivityState.waiting_duration)
async def process_duration(message: Message, state: FSMContext):

    try:
        input_number = int(message.text)
        if input_number <= 0:
            await message.answer('Продолжительность должна быть больше 0')
            return
        elif input_number > 600:
            await message.answer('Не может быть!')
            return

        await state.update_data(duration=input_number)
        await message.answer("Выберите часть дня", reply_markup=type_of_date_button_keyboard())
        await state.set_state(ActivityState.waiting_daypart)
        
    except Exception as e:
        print(e)
        await message.answer("Продолжительность должна быть числом")
        return


@router.message(ActivityState.waiting_daypart)
async def process_daypart(message: Message, state: FSMContext, session: AsyncSession):

    await state.update_data(daypart=message.text)
    await state.set_state(ActivityState.waiting_activity_type)
    await message.answer("Выберите вид активности", reply_markup=await activity_types_keyboard(session=session))


@router.message(ActivityState.waiting_activity_type)
async def process_activity_type(message: Message, state: FSMContext, session: AsyncSession):

    activity_type_name = message.text

    activity_type = await activity_type_crud.get_by_attribute(
        'activity_type_name',
        activity_type_name,
        session=session
    )

    await state.set_state(ActivityState.waiting_activity_sybtype)
    await message.answer(
        "Выберите тип активности",
        reply_markup=await activity_subtypes_keyboard(session, activity_type.id)
    )


@router.callback_query(ActivityState.waiting_activity_sybtype, F.data.startswith("activity_subtype:"))
async def process_activity_add(callback: CallbackQuery, state: FSMContext, session: AsyncSession):

    activity_subtype_id = callback.data.split(':')[-1]
    activity_subtype_obj = await activity_subtype_crud.get(int(activity_subtype_id), session)

    await state.update_data(activity_subtype=activity_subtype_obj)

    data = await state.get_data()
    print(data)

    await activity_crud.create(session, data)

    await callback.answer("Данные добавлены")
    await callback.message.edit_text("Данные добавлены")

    await state.clear()


@router.callback_query(F.data == "cancel")
async def cancel_survey(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Опрос отменен")
    await callback.answer()
