import io
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.database import get_sleep_data

def fetch_sleep_data(user_id: int, days: int = 7) -> pd.DataFrame:
    data = get_sleep_data(user_id, days)
    if not data:
        return pd.DataFrame()

    records = []
    for row in data:
        day       = row['date']        # datetime.date
        sleep_dt  = row['sleep_time']  # datetime.datetime
        wake_dt   = row['wake_time']   # datetime.datetime

        if wake_dt <= sleep_dt:
            wake_dt += timedelta(days=1)

        dur = (wake_dt - sleep_dt).total_seconds() / 3600
        records.append({
            'date': pd.to_datetime(day),           # в datetime64
            'duration': round(dur, 2)
        })

    df = pd.DataFrame(records)
    df = df.sort_values('date')
    return df

def create_sleep_chart(df: pd.DataFrame) -> io.BytesIO:
    if df.empty:
        raise ValueError("Нет данных для построения графика")

    dates = df['date']  # серия datetime64[ns]
    durations = df['duration']

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))

    # зона 6.5–9.5 ч
    ax.axhspan(6.5, 9.5, color='green', alpha=0.1)
    ax.axhline(8, linestyle='--', alpha=0.3, color='green')

    # график
    ax.plot(dates, durations, marker='o', linestyle='-', linewidth=2, markersize=8)

    # подписи над точками
    for x, y in zip(dates, durations):
        ax.text(x, y + 0.2, f"{y} ч", ha='center', fontsize=8)

    # явно задаём метки и пределы по X
    ax.set_xlim(dates.min(), dates.max())
    ax.set_xticks(dates)

    # формат отображения дат
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))

    # подпись осей и заголовок
    ax.set_xlabel('Дата')
    ax.set_ylabel('Часы сна')
    ax.set_title('Ваш сон за последние 7 дней', pad=20)

    ax.set_ylim(0, 12)
    ax.grid(alpha=0.3)

    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120)
    buf.seek(0)
    plt.close(fig)
    return buf
