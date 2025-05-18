# database.py
import sqlite3
from datetime import datetime, timedelta
from config import DB_PATH


def init_db():
    conn = sqlite3.connect('data/habitquest.db')
    c = conn.cursor()


    c.execute('''CREATE TABLE IF NOT EXISTS sleep_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        sleep_time TEXT,
        wake_time TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        level TEXT,
        exercises TEXT
    )''')


    c.execute('''CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        reminder_time TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()


def save_workout(user_id: int, level: str, exercises: str):
    conn = sqlite3.connect('data/habitquest.db')
    c = conn.cursor()

    c.execute('''INSERT INTO workouts (user_id, date, level, exercises)
                 VALUES (?, ?, ?, ?)''',
              (user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), level, exercises))

    conn.commit()
    conn.close()


def get_user_workouts(user_id: int, limit: int = 5):
    conn = sqlite3.connect('data/habitquest.db')
    c = conn.cursor()

    c.execute('''SELECT date, level, exercises
                 FROM workouts
                 WHERE user_id = ?
                 ORDER BY date DESC
                 LIMIT ?''', (user_id, limit))

    results = c.fetchall()
    conn.close()
    return results

def save_sleep_data(user_id: int, sleep_time: str, wake_time: str):
    now = datetime.now()
    sleep_dt = datetime.strptime(sleep_time, '%H:%M')
    wake_dt = datetime.strptime(wake_time, '%H:%M')

    # Привязываем дату к sleep_time — сегодня или вчера
    sleep_datetime = now.replace(hour=sleep_dt.hour, minute=sleep_dt.minute, second=0, microsecond=0)
    if sleep_datetime > now:
        sleep_datetime -= timedelta(days=1)

    # wake_time считается на следующий день, если раньше sleep_time
    wake_datetime = now.replace(hour=wake_dt.hour, minute=wake_dt.minute, second=0, microsecond=0)
    if wake_datetime <= sleep_datetime:
        wake_datetime += timedelta(days=1)

    # Сохраняем
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        '''INSERT INTO sleep_data (user_id, sleep_time, wake_time)
           VALUES (?, ?, ?)''',
        (user_id, sleep_datetime.strftime('%Y-%m-%d %H:%M'), wake_datetime.strftime('%Y-%m-%d %H:%M'))
    )
    conn.commit()
    conn.close()


def get_sleep_data(user_id: int, days: int = 7):
    from datetime import datetime, timedelta
    conn = sqlite3.connect('data/habitquest.db')
    c = conn.cursor()
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    c.execute('''
        SELECT date(sleep_time), sleep_time, wake_time
        FROM sleep_data
        WHERE user_id = ? AND date(sleep_time) >= ?
        ORDER BY sleep_time ASC
    ''', (user_id, since))
    rows = c.fetchall()
    conn.close()
    return rows