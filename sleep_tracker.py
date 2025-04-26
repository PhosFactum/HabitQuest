from aiogram import types, Dispatcher
from database import get_db

async def set_sleep_time(message: types.Message):
    # Логика сохранения времени сна
    pass

async def set_wake_time(message: types.Message):
    # Логика сохранения времени пробуждения
    pass

def register_sleep_handlers(dp: Dispatcher):
    dp.register_message_handler(set_sleep_time, commands=["set_sleep"])
    dp.register_message_handler(set_wake_time, commands=["set_wake"])