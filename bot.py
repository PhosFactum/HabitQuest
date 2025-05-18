# bot.py
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from database import init_db
from scheduler import start_scheduler
from handlers import register_handlers


logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("TOKEN")


async def main():
    # Initialize database and scheduler
    init_db()
    start_scheduler()  # Теперь переменная определена

    # Initialize bot and dispatcher
    storage = MemoryStorage()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)

    # Register all handlers
    register_handlers(dp)

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())