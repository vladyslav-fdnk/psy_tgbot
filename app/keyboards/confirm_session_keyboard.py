from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data="confirm_booking",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data="cancel_booking",
                )
            ],
        ]
    )
