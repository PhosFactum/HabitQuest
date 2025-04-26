import random


def generate_workout(level="средняя"):
    base = {
        "лёгкая": ["Приседания x10", "Планка 30 сек", "Прыжки x10"],
        "средняя": ["Приседания x20", "Планка 60 сек", "Прыжки x20"],
        "тяжёлая": ["Бёрпи x15", "Планка 90 сек", "Приседания с прыжком x15"]
    }

    exercises = base.get(level, base["средняя"])
    random.shuffle(exercises)  # Перемешиваем упражнения

    workout_text = "\n".join(exercises)  # Объединяем упражнения
    workout_text += "\n\n🔁 Повторить всё 4 раза"  # Добавляем подходы

    return workout_text