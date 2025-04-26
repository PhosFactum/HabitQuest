from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛌 Сон")],
            [KeyboardButton(text="🏋️ Тренировка")],
            [KeyboardButton(text="ℹ️ Совет")]
        ],
        resize_keyboard=True
    )
    return keyboard

def workout_levels_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💚 Лёгкая", callback_data="level_easy"),
                InlineKeyboardButton(text="💪 Средняя", callback_data="level_medium"),
                InlineKeyboardButton(text="🔥 Тяжёлая", callback_data="level_hard"),
            ]
        ]
    )
    return keyboard
