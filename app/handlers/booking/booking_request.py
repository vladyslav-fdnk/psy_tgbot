import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from dotenv import load_dotenv


from app.database.db import add_booking, get_client_id


load_dotenv()


psy_id = int(os.getenv("PSYCHOLOGIST_ID", "0"))

if not psy_id:
    raise ValueError("PSYCHOLOGIST_ID is not set")

router = Router()


@router.callback_query(F.data == "confirm_booking")
async def confirm_booking(
    callback: CallbackQuery,
    state: FSMContext,
):
    data = await state.get_data()

    user = callback.from_user
    client_id = get_client_id(user.id)

    if client_id is None:
        return

    add_booking(
        client_id=client_id,
        service=data["service"],
        date=data["date"],
        time=data["time"],
        status="pending",
    )

    if callback.message:
        await callback.message.answer(
            "🕒 Ваша запись отправлена на подтверждение психологу.\n"
            "Мы уведомим вас после проверки."
        )

    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "cancel_booking")
async def cancel_booking(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.clear()

    if callback.message:
        await callback.message.answer("❌ Запись отменена")

    await callback.answer()


async def notify_psychologist(
    callback: CallbackQuery,
    data: dict,
    client_id: int,
):
    text = "\n".join(
        [
            "Новая заявка:\n",
            f"👤 Клиент: {client_id}",
            f"📅 Дата: {data['date']}",
            f"🕒 Время: {data['time']}",
            f"🧠 Услуга: {data['service']}",
        ]
    )
    bot = callback.bot
    if bot is None:
        return

    await bot.send_message(
        chat_id=psy_id,
        text=text,
    )
