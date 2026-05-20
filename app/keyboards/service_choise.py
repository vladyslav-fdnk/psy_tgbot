from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_service_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟢 Ознакомительная (15-20 минут)",
                    callback_data="service_intro",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔵 Индивидуальная (50-60 минут)",
                    callback_data="service_individual",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟣 Парная (50-60 минут)", callback_data="service_couple"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔴 Экстренная", callback_data="service_urgent"
                )
            ],
        ]
    )
