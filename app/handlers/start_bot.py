from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

from app.keyboards.main_menu import main_menu

router = Router()

@router.message(CommandStart())
async def start_bot(message: Message):

    name = message.from_user.first_name
    text = (
        f"👋 <b>Привет, {name}!</b>\n\n"
        "Я помогу вам:\n"
        "• записаться на консультацию\n"
        "• заполнить анкету\n"
        "• вести дневник настроения\n\n"
        "Выберите действие ниже 👇"
    )
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=main_menu
    )