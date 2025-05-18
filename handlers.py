import logging

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from sleep.reminders import set_sleep_reminder
from sleep.advice import get_sleep_advice
from workout.generator import generate_workout
from keyboards import main_menu_keyboard, workout_levels_keyboard
from database import save_workout, get_user_workouts

# FSM states for sleep time input
class SleepStates(StatesGroup):
    waiting_for_sleep_time = State()


def register_handlers(dp):
    # Command handlers
    dp.message.register(send_welcome, Command("start"))
    dp.message.register(handle_sleep_command, Command("sleep"))
    dp.message.register(handle_train_command, Command("train"))
    dp.message.register(handle_my_trainings, Command("mytrainings"))

    # Text buttons
    dp.message.register(handle_sleep_text, F.text == "🛌 Сон")
    dp.message.register(process_sleep_time, StateFilter(SleepStates.waiting_for_sleep_time))
    dp.message.register(handle_train_text, F.text == "🏋️ Тренировка")
    dp.message.register(handle_advice, F.text == "ℹ️ Совет")
    dp.message.register(handle_my_trainings_button, F.text == "📖 Мои тренировки")

    # Callback query for workout level selection
    dp.callback_query.register(handle_level_callback, F.data.startswith("level_"))


# Handlers implementations
async def send_welcome(message: Message):
    await message.answer(
        "Привет! Я — HabitQuest, твой помощник по ЗОЖ. Выбери действие:",
        reply_markup=main_menu_keyboard()
    )

async def handle_sleep_command(message: Message, state: FSMContext):
    await handle_sleep_text(message)

async def handle_train_command(message: Message):
    await handle_train_text(message)

async def handle_my_trainings(message: Message):
    await handle_my_trainings_button(message)

async def handle_sleep_text(message: Message):
    await message.answer("Напоминание на сон установлено! Желаю сладких снов 😴")
    # Ask for sleep time or set default
    await set_sleep_reminder(message)

async def process_sleep_time(message: Message, state: FSMContext):
    await set_sleep_reminder(message, message.text)
    await state.clear()

async def handle_train_text(message: Message):
    await message.answer(
        "Выбери уровень тренировки:",
        reply_markup=workout_levels_keyboard()
    )

async def handle_advice(message: Message):
    advice = get_sleep_advice()
    await message.answer(f"Совет по сну: {advice}")

async def handle_my_trainings_button(message: Message):
    workouts = get_user_workouts(message.from_user.id)

    if not workouts:
        await message.answer("У тебя пока нет сохранённых тренировок 💤")
        return

    response = "🏋️‍♂️ Твои последние тренировки:\n\n"
    for date, level, exercises in workouts:
        response += (
            f"📅 {date}\n"
            f"🔸 Уровень: {level.title()}\n"
            f"📋 Упражнения:\n{exercises}\n\n"
        )

    await message.answer(response.strip())

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
