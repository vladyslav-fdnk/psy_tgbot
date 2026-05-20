import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


def create_bot() -> Bot:
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is not set")

    return Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
