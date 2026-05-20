from datetime import date

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram_calendar import (
    SimpleCalendar,
    SimpleCalendarCallback,
)

from app.handlers.booking.booking_states import BookingState
from app.keyboards.time_session_keyboard import get_time_keyboard


router = Router()


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

    if not selected or not selected_date:
        await callback.answer()
        return

    if selected_date.date() < date.today():
        if callback.message:
            await callback.message.answer(
                "❌ Нельзя выбрать прошедшую дату. Выберите другую дату."
            )
        await callback.answer()
        return

    selected_date = selected_date.strftime("%Y-%m-%d")

    await state.update_data(date=selected_date)
    await state.set_state(BookingState.time)

    if not callback.message:
        return

    await callback.message.answer(
        f"📅 Вы выбрали дату: {selected_date}\n⏰ Теперь выберите время:",
        reply_markup=get_time_keyboard(),
    )

    await callback.answer()
