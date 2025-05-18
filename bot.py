import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN
from database import init_db
from handlers import register_handlers

logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize database and scheduler
    init_db()
    scheduler = AsyncIOScheduler()
    scheduler.start()

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