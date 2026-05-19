from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from app.handlers.start_bot import router as start_router
from app.handlers.booking import router as booking_router

import asyncio
import os

load_dotenv()

bot = Bot(
    token=os.getenv("BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(booking_router)


async def main():
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())