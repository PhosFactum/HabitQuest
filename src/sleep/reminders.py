# sleep/reminders.py
from aiogram import Bot
from aiogram.types import Message
from datetime import datetime, timedelta
from src.scheduler import scheduler
from config import TOKEN


async def send_sleep_alert(chat_id: int):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id, "Пора спать! 😴")
    await bot.session.close()

async def set_sleep_reminder(message: Message, time_str: str = None):
    """
    Если time_str не передан — сразу ставим на дефолт (через 10 секунд).
    Иначе парсим HH:MM для установки точного времени.
    """
    now = datetime.now()
    if not time_str:
        run_dt = now + timedelta(seconds=10)
    else:
        try:
            t = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            await message.answer("Неверный формат. Введи время в формате HH:MM.")
            return
        run_dt = datetime.combine(now.date(), t)
        if run_dt <= now:
            run_dt += timedelta(days=1)

    job_id = f"sleep_{message.chat.id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    scheduler.add_job(
        send_sleep_alert,
        trigger="date",
        run_date=run_dt,
        args=[message.chat.id],
        id=job_id,
    )
    await message.answer(f"Напоминание поставлено на {run_dt.strftime('%H:%M — %d.%m.%Y')}")