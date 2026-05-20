from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.handlers.booking.booking_states import BookingState
from app.keyboards.service_choise import get_service_keyboard


router = Router()


@router.message((F.text == "📅 Записаться") | (F.text == "/booking"))
async def booking(message: Message, state: FSMContext):
    await state.clear()

    await state.set_state(BookingState.service)

    await message.answer(
        "Выберите тип консультации:",
        reply_markup=get_service_keyboard(),
    )
