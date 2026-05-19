from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from app.handlers.start_bot import router as start_router
from app.handlers.booking import router as booking_router
from app.handlers.client_form import router as client_form_router

from app.database.db import init_db

import asyncio
import os

load_dotenv()

token = os.getenv("BOT_TOKEN")
if not token:
    raise ValueError("BOT_TOKEN is not set")

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(booking_router)
dp.include_router(client_form_router)


async def main():
    init_db()

    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
