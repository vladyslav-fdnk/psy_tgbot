from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram_calendar import SimpleCalendar

from app.handlers.booking.booking_states import BookingState


router = Router()


@router.callback_query(F.data.startswith("service_"))
async def process_service(callback: CallbackQuery, state: FSMContext):

    if not callback.data:
        return

    service = callback.data.replace("service_", "")

    await state.update_data(service=service)
    await state.set_state(BookingState.date)

    if not callback.message:
        return

    await callback.message.answer(
        "Выберите дату консультации 📅",
        reply_markup=await SimpleCalendar().start_calendar(),
    )

    await callback.answer()
