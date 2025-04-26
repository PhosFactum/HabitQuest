from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN
from sleep.reminders import set_sleep_reminder
from sleep.advice import get_sleep_advice
from workout.generator import generate_workout
from keyboards import main_menu_keyboard, workout_levels_keyboard
from database import init_db
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        "Привет! Я — HabitQuest, твой помощник по ЗОЖ. Выбери действие:",
        reply_markup=main_menu_keyboard()
    )

@dp.message(Command("sleep"))
async def handle_sleep_command(message: Message):
    await handle_sleep(message)

@dp.message(Command("train"))
async def handle_train_command(message: Message):
    await handle_train(message)

@dp.message(F.text == "🛌 Сон")
async def handle_sleep(message: Message):
    await message.answer("Напоминание на сон установлено! Желаю сладких снов 😴")
    await set_sleep_reminder(message)

@dp.message(F.text == "🏋️ Тренировка")
async def handle_train(message: Message):
    await message.answer(
        "Выбери уровень тренировки:",
        reply_markup=workout_levels_keyboard()
    )

@dp.message(F.text == "ℹ️ Совет")
async def handle_advice(message: Message):
    advice = get_sleep_advice()
    await message.answer(f"Совет по сну: {advice}")

# Обработчики inline-кнопок выбора уровня
@dp.callback_query(F.data.startswith("level_"))
async def handle_level_callback(callback: CallbackQuery):
    level_mapping = {
        "level_easy": "лёгкая",
        "level_medium": "средняя",
        "level_hard": "тяжёлая"
    }
    selected_level = level_mapping.get(callback.data)
    workout = generate_workout(level=selected_level)
    await callback.message.answer(f"Твоя тренировка ({selected_level.title()}):\n{workout}")
    await callback.answer()  # Закрыть "часики" на кнопке

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())