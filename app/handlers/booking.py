from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.database.db import add_booking


router = Router()


class BookingState(StatesGroup):
    date = State()
    time = State()


def get_time_keyboard():
    time_slots = ["10:30", "12:00", "13:30", "14:30", "15:00", "16:30"]

    keyboard = [
        [InlineKeyboardButton(text=slot, callback_data=f"time_{slot}")]
        for slot in time_slots
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.message(F.text == "📅 Записаться")
async def booking(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "Выберите дату консультации 📅",
        reply_markup=await SimpleCalendar().start_calendar(),
    )


@router.callback_query(SimpleCalendarCallback.filter())
async def process_calendar(
    callback: CallbackQuery,
    callback_data: SimpleCalendarCallback,
    state: FSMContext,
):
    selected, selected_date = await SimpleCalendar().process_selection(
        callback,
        callback_data,
    )

    if selected:
        selected_date = selected_date.strftime("%Y-%m-%d")

        await state.update_data(date=selected_date)
        await state.set_state(BookingState.time)

        if not callback.message:
            return

        await callback.message.answer(
            f"Вы выбрали дату: {selected_date}\nТеперь выберите время:",
            reply_markup=get_time_keyboard(),
        )

    await callback.answer()


@router.callback_query(F.data.startswith("time_"))
async def process_time_(callback: CallbackQuery, state: FSMContext):

    if not callback.data:
        return

    time = callback.data.replace("time_", "")

    data = await state.get_data()
    selected_date = data.get("date")

    if not selected_date:
        message = callback.message
        if message is None:
            return

        await message.answer(
            "Дата не найдена. Начните бронирование заново через /booking"
        )
        await callback.answer()
        return

    await state.update_data(time=time)

    if not callback.message:
        return

    user = callback.from_user

    add_booking(
        user_id=user.id,
        username=user.username or "",
        date=selected_date,
        time=time,
    )

    await callback.message.answer(
        f"Вы выбрали:\n"
        f"Дата: {selected_date}\n"
        f"Время: {time}\n\n"
        f"Бронирование оформлено ✅"
    )

    await state.clear()
    await callback.answer()
