import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from sleep.reminders import set_sleep_reminder
from sleep.advice import get_sleep_advice
from workout.generator import generate_workout
from keyboards import main_menu_keyboard, workout_levels_keyboard
from database import init_db, save_workout, get_user_workouts
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

logging.basicConfig(level=logging.INFO)


# Инициализация FSM состояний
class SleepStates(StatesGroup):
    waiting_for_sleep_time = State()


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

# Создаём планировщик
scheduler = AsyncIOScheduler()


@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        "Привет! Я — HabitQuest, твой помощник по ЗОЖ. Выбери действие:",
        reply_markup=main_menu_keyboard()
    )


@dp.message(Command("sleep"))
async def handle_sleep_command(message: Message, state: FSMContext):
    await handle_sleep(message, state)


@dp.message(Command("train"))
async def handle_train_command(message: Message):
    await handle_train(message)


@dp.message(Command("mytrainings"))
async def handle_my_trainings(message: Message):
    await handle_my_trainings_button(message)


@dp.message(F.text == "🛌 Сон")
async def handle_sleep(message: Message):
    await message.answer("Напоминание на сон установлено! Желаю сладких снов 😴")
    await set_sleep_reminder(message)


@dp.message(SleepStates.waiting_for_sleep_time)
async def process_sleep_time(message: Message, state: FSMContext):
    await set_sleep_reminder(message, message.text)
    await state.clear()


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


@dp.message(F.text == "📖 Мои тренировки")
async def handle_my_trainings_button(message: Message):
    workouts = get_user_workouts(message.from_user.id)

    if not workouts:
        await message.answer("У тебя пока нет сохранённых тренировок 💤")
        return

    response = "🏋️‍♂️ Твои последние тренировки:\n\n"
    for date, level, exercises in workouts:
        response += f"📅 {date}\n🔸 Уровень: {level.title()}\n📋 Упражнения:\n{exercises}\n\n"

    await message.answer(response.strip())


@dp.callback_query(F.data.startswith("level_"))
async def handle_level_callback(callback: CallbackQuery):
    level_mapping = {
        "level_easy": "лёгкая",
        "level_medium": "средняя",
        "level_hard": "тяжёлая"
    }
    selected_level = level_mapping.get(callback.data)
    workout = generate_workout(level=selected_level)

    save_workout(
        user_id=callback.from_user.id,
        level=selected_level,
        exercises=workout
    )

    await callback.message.answer(f"Твоя тренировка ({selected_level.title()}):\n{workout}")
    await callback.answer()


async def main():
    # Инициализация базы данных
    init_db()

    # Запуск планировщика после инициализации базы данных
    scheduler.start()

    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Запуск основного цикла
    asyncio.run(main())
