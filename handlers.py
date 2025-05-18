# handlers.py
import io
import pandas as pd
import matplotlib.pyplot as plt

from aiogram import F, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sleep.reminders import set_sleep_reminder
from sleep.advice import get_sleep_advice
from workout.generator import generate_workout
from keyboards import (
    main_menu_keyboard,
    sleep_menu_keyboard,
    workout_levels_keyboard,
)
from database import (
    save_workout,
    get_user_workouts,
    save_sleep_data,
    get_sleep_stats,
)

# Define FSM states for sleep
class SleepStates(StatesGroup):
    waiting_for_sleep_time = State()
    waiting_for_sleep_input = State()

async def send_welcome(message: Message):
    # Greet the user and show main menu
    await message.answer(
        "Привет! Я — HabitQuest, твой помощник по ЗОЖ. Выбери действие:",
        reply_markup=main_menu_keyboard(),
    )

async def handle_sleep_command(message: Message, state: FSMContext):
    # Open sleep submenu
    await show_sleep_menu(message)

async def show_sleep_menu(message: Message):
    # Display sleep options
    await message.answer(
        "Выберите опцию по сну:",
        reply_markup=sleep_menu_keyboard(),
    )

async def handle_sleep_menu(message: Message, state: FSMContext):
    # Handle user selection in sleep submenu
    text = message.text
    if text == "🛌 Напоминание":
        # Ask user for reminder time
        await message.answer("Во сколько поставить напоминание? Введите время в формате HH:MM")
        await state.set_state(SleepStates.waiting_for_sleep_time)
    elif text == "⏰ Ввести время сна":
        # Prompt user to log sleep interval
        await message.answer("Введите время сна и подъёма в формате HH:MM-HH:MM")
        await state.set_state(SleepStates.waiting_for_sleep_input)
    elif text == "📊 Статистика":
        # Show sleep statistics
        await show_sleep_stats(message)
    elif text == "↩️ Назад":
        # Return to main menu
        await message.answer("Главное меню:", reply_markup=main_menu_keyboard())
        await state.clear()

async def process_sleep_time(message: Message, state: FSMContext):
    # Process reminder time input and schedule
    time_str = message.text.strip()
    await set_sleep_reminder(message, time_str)
    await state.clear()

async def process_sleep_input(message: Message, state: FSMContext):
    # Process logging of sleep interval
    try:
        sleep_str, wake_str = message.text.split('-')
    except ValueError:
        await message.answer("Неверный формат. Пример: 22:30-06:45")
        return
    save_sleep_data(
        user_id=message.from_user.id,
        sleep_time=sleep_str.strip(),
        wake_time=wake_str.strip(),
    )
    await message.answer("Время сна сохранено! 💤", reply_markup=main_menu_keyboard())
    await state.clear()

async def show_sleep_stats(message: Message):
    # Build and send sleep duration chart for last 7 days
    stats = get_sleep_stats(message.from_user.id)
    if not stats:
        await message.answer("Нет данных для статистики.", reply_markup=main_menu_keyboard())
        return
    df = pd.DataFrame(stats)
    fig, ax = plt.subplots()
    ax.axhspan(7, 9, alpha=0.2)
    ax.plot(df['date'], df['duration'], marker='o')
    ax.set_title('Сон за последние 7 дней')
    ax.set_ylabel('Часы сна')
    ax.set_xlabel('Дата')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    await message.answer_photo(types.InputFile(buf, filename='sleep_stats.png'), reply_markup=main_menu_keyboard())
    buf.close()

async def handle_train_command(message: Message):
    # Redirect to training menu
    await handle_train_text(message)

async def handle_train_text(message: Message):
    # Show workout levels
    await message.answer(
        "Выбери уровень тренировки:",
        reply_markup=workout_levels_keyboard(),
    )

async def handle_advice(message: Message):
    # Send sleep advice
    advice = get_sleep_advice()
    await message.answer(f"Совет по сну: {advice}")

async def handle_my_trainings_command(message: Message):
    # Redirect to my trainings
    await handle_my_trainings_button(message)

async def handle_my_trainings_button(message: Message):
    # Show user's saved workouts
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
    # Generate and save workout based on level
    mapping = {"level_easy": "лёгкая", "level_medium": "средняя", "level_hard": "тяжёлая"}
    level = mapping.get(callback.data)
    workout = generate_workout(level=level)
    save_workout(
        user_id=callback.from_user.id,
        level=level,
        exercises=workout,
    )
    await callback.message.answer(f"Твоя тренировка ({level.title()}):\n{workout}")
    await callback.answer()