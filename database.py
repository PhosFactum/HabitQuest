import sqlite3

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

    conn.commit()
    conn.close()
