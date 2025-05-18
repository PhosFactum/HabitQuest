# sleep/reminders.py
from aiogram import Bot
from datetime import timedelta
from scheduler import scheduler
from config import TOKEN  # <-- импорт вашего токена

async def send_sleep_alert(chat_id: int):
    # создаём бота «на лету» и сразу после отправки закрываем сессию
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id, "Пора спать! 😴")
    await bot.session.close()  # важно чтобы не накапливались соединения

async def set_sleep_reminder(message, time_str: str):
    from datetime import datetime  # для краткости

    # Парсим HH:MM, считаем run_date
    try:
        t = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        await message.answer("Неверный формат, нужно HH:MM.")
        return

    now = datetime.now()
    run_dt = datetime.combine(now.date(), t)
    if run_dt <= now:
        run_dt += timedelta(days=1)

    job_id = f"sleep_{message.chat.id}"
    # Удаляем старое
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    # Регистрируем новую корутину
    scheduler.add_job(
        send_sleep_alert,
        "date",
        run_date=run_dt,
        args=[message.chat.id],
        id=job_id,
    )

    await message.answer(f"Напоминание поставлено на {run_dt.strftime('%H:%M — %d.%m.%Y')}")
