from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Записаться")],
        [KeyboardButton(text="🧠 Мое состояние")],
        [KeyboardButton(text="📓 Дневник")],
        [KeyboardButton(text="💬 Написать психологу")],
        [KeyboardButton(text="📚 Материалы")],
        [KeyboardButton(text="💳 Оплата")],
        [KeyboardButton(text="ℹ️ О специалисте")],

    ],
    resize_keyboard=True
)