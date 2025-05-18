# sleep/charts.py
import io
from datetime import datetime, timedelta

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from database import get_sleep_data


def fetch_sleep_data(user_id: int, days: int = 7) -> pd.DataFrame:
    data = get_sleep_data(user_id, days)

    if not data:
        return pd.DataFrame()

    sleep_records = []
    for date_str, sleep_str, wake_str in data:
        sleep_dt = datetime.strptime(sleep_str, '%Y-%m-%d %H:%M')
        wake_dt = datetime.strptime(wake_str, '%Y-%m-%d %H:%M')

        if wake_dt <= sleep_dt:
            wake_dt += timedelta(days=1)

        duration = (wake_dt - sleep_dt).total_seconds() / 3600
        sleep_records.append({
            'date': date_str,
            'duration': round(duration, 2),
            'sleep_time': sleep_str,
            'wake_time': wake_str
        })

    return pd.DataFrame(sleep_records)


def create_sleep_chart(df: pd.DataFrame) -> io.BytesIO:
    """Создает график сна и возвращает его как BytesIO"""
    if df.empty:
        raise ValueError("Нет данных для построения графика")

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    # Оптимальная зона сна (7-9 часов)
    ax.axhspan(6.5, 9.5, color='green', alpha=0.1)
    ax.axhline(y=8, color='green', linestyle='--', alpha=0.3)

    # График сна
    ax.plot(df['date'], df['duration'],
            marker='o',
            linestyle='-',
            color='blue',
            markersize=8,
            linewidth=2)

    # Подписи точек
    for i, row in df.iterrows():
        ax.text(row['date'], row['duration'] + 0.2,
                f"{row['duration']} ч",
                ha='center',
                fontsize=8)

    # Настройки графика
    ax.set_title('Ваш сон за последние 7 дней', pad=20)
    ax.set_ylabel('Часы сна')
    ax.set_xlabel('Дата')
    ax.set_ylim(0, 12)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Сохраняем в буфер
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120)
    buf.seek(0)
    plt.close(fig)

    return buf