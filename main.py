from aiogram import Dispatcher, Router
from dotenv import load_dotenv

from app.config.bot import create_bot
from app.handlers.booking.router import booking_router

from app.handlers.start_bot import router as start_bot_router
from app.handlers.client_form import router as client_form_router

from app.database.db import init_db

import asyncio

load_dotenv()

router = Router()
bot = create_bot()
dp = Dispatcher()

dp.include_router(booking_router)
dp.include_router(start_bot_router)
dp.include_router(client_form_router)


async def main():
    init_db()
    print("Bot started")
    print("booking_router:", booking_router)
    print(booking_router.parent_router)
    # dp.include_router(booking_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
