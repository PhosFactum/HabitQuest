# src/workout/levels.py
def get_available_levels():
    return ["лёгкая", "средняя", "тяжёлая"]

def describe_level(level):
    descriptions = {
        "лёгкая": "Подходит для новичков или для восстановления.",
        "средняя": "Поддержание хорошей физической формы.",
        "тяжёлая": "Интенсивные тренировки для продвинутых."
    }
    return descriptions.get(level, "Уровень не найден.")
