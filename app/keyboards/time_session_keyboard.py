from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_time_keyboard():
    time_slots = [
        "10:30",
        "12:00",
        "13:30",
        "14:30",
        "15:00",
        "16:30",
    ]

    keyboard = [
        [
            InlineKeyboardButton(
                text=slot,
                callback_data=f"time_{slot}",
            )
        ]
        for slot in time_slots
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
