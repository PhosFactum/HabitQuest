from aiogram.types import Message
from datetime import datetime, timedelta
import asyncio

async def set_sleep_reminder(message: Message):
    # Фиктивная логика: напомнить через 10 секунд
    await asyncio.sleep(10)
    await message.answer("Пора спать! 😴")
