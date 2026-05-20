from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.database.db import get_client_id

from app.keyboards.cliern_form_button import (
    get_client_form_keyboard,
)
from app.keyboards.confirm_session_keyboard import (
    get_confirm_keyboard,
)
from app.handlers.booking.booking_states import BookingState


router = Router()


@router.callback_query(F.data.startswith("time_"))
async def process_time_(callback: CallbackQuery, state: FSMContext):

    if not callback.data:
        return

    time_str = callback.data.replace("time_", "")

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

    today_str = datetime.now().strftime("%Y-%m-%d")

    if selected_date == today_str:
        now = datetime.now().strftime("%H:%M")

        if time_str < now:
            if callback.message:
                await callback.message.answer(
                    "❌ Нельзя выбрать прошедшее время. Выберите другое."
                )
            await callback.answer()
            return

    await state.update_data(time=time_str)

    if not callback.message:
        return

    user = callback.from_user

    # print("DEBUG telegram user id:", user.id)

    client_id = get_client_id(user.id)

    if client_id is None:
        await callback.message.answer(
            "Сначала заполните анкету клиента",
            reply_markup=get_client_form_keyboard(),
        )
        await callback.answer()
        return

    # print("DEBUG client_id:", client_id)
    # print("DEBUG date:", selected_date)
    # print("DEBUG time:", time_str)

    await state.set_state(BookingState.confirm)

    data = await state.get_data()
    service = data.get("service")
    if service is None:
        return

    service_names = {
        "intro": "🟢 Ознакомительная",
        "individual": "🔵 Индивидуальная",
        "couple": "🟣 Парная",
        "urgent": "🔴 Экстренная",
    }

    service_text = service_names.get(service, service)

    await callback.message.answer(
        f"📋 Подтверждение записи\n\n"
        f"Услуга: {service_text}\n"
        f"Дата: {selected_date}\n"
        f"Время: {time_str}\n\n"
        f"Подтвердить запись?",
        reply_markup=get_confirm_keyboard(),
    )

    await callback.answer()
    return

    await callback.message.answer(
        f"Вы выбрали:\n"
        f"Дата: {selected_date}\n"
        f"Время: {time_str}\n\n"
        f"Бронирование оформлено ✅"
    )

    await state.clear()
    await callback.answer()


# print(get_client_id(5922576108))
