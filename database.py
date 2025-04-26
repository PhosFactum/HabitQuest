import sqlite3
from datetime import datetime


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


