from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_client_form_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Заполнить анкету",
                    callback_data="fill_form",
                )
            ]
        ]
    )
