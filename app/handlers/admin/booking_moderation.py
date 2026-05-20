from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.database.db import approve_booking_in_db, reject_booking_in_db, get_client_id

router = Router()


@router.callback_query(F.data.startswith("approve_"))
async def approve_booking(callback: CallbackQuery):

    if not callback.data:
        return
    booking_id = int(callback.data.split("_")[1])

    approve_booking_in_db(booking_id)

    if callback.message is None or not hasattr(callback.message, "edit_text"):
        return

    client_id = get_client_id(booking_id)
    if client_id is None:
        return

    bot = callback.bot
    if bot is None:
        return

    async def handler():
        await bot.send_message(client_id, "✅ Психолог подтвердил вашу запись!")

    if callback.message and hasattr(callback.message, "edit_text"):
        await callback.message.edit_text("✅ Запись подтверждена психологом")


@router.callback_query(F.data.startswith("reject_"))
async def reject_booking(callback: CallbackQuery):

    if not callback.data:
        return
    booking_id = int(callback.data.split("_")[1])

    reject_booking_in_db(booking_id)
    client_id = get_client_id(booking_id)

    bot = callback.bot
    if bot is None:
        return

    async def handler():
        await bot.send_message(
            client_id, "❌ Ваша запись отклонена. Выберите другое время."
        )

    if callback.message and hasattr(callback.message, "edit_text"):
        await callback.message.edit_text("❌ Запись отклонена")
    await callback.answer()
