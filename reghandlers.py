# reghandlers.py
from aiogram import F, Dispatcher
from aiogram.filters import Command, StateFilter

from handlers import (
    send_welcome,
    handle_sleep_command,
    show_sleep_menu,
    handle_sleep_menu,
    process_sleep_time,
    process_sleep_input,
    show_sleep_stats,
    handle_train_command,
    handle_train_text,
    handle_advice,
    handle_my_trainings_command,
    handle_my_trainings_button,
    handle_level_callback,
    SleepStates,
)

def register_handlers(dp: Dispatcher):
    # Register command handlers
    dp.message.register(send_welcome, Command("start"))
    dp.message.register(handle_sleep_command, Command("sleep"))
    dp.message.register(handle_train_command, Command("train"))
    dp.message.register(handle_my_trainings_command, Command("mytrainings"))

    # Register main menu interactions
    dp.message.register(show_sleep_menu, F.text == "🛌 Сон")
    dp.message.register(handle_train_text, F.text == "🏋️ Тренировка")
    dp.message.register(handle_advice, F.text == "ℹ️ Совет по сну")
    dp.message.register(handle_my_trainings_button, F.text == "📖 Мои тренировки")

    # Register sleep submenu interactions
    dp.message.register(
        handle_sleep_menu,
        F.text.in_(["🛌 Напоминание", "⏰ Ввести время сна", "📊 Статистика", "↩️ Назад"])
    )
    dp.message.register(
        process_sleep_time,
        StateFilter(SleepStates.waiting_for_sleep_time)
    )
    dp.message.register(
        process_sleep_input,
        StateFilter(SleepStates.waiting_for_sleep_input)
    )

    # Register workout level callbacks
    dp.callback_query.register(handle_level_callback, F.data.startswith("level_"))
