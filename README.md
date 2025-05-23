## HabitQuest - Бот для здоровых привычек

### 🌟 **Возможности бота**

***HabitQuest помогает вырабатывать полезные привычки через Telegram:*** 

#### 🛌 **Умный трекер сна:**

- Напоминания о времени отхода ко сну

- Персональные рекомендации по улучшению сна

- Анализ вашего режима сна

#### 🏋️ **Персональный тренер:**

- 3 уровня тренировок: от новичка до профи

- Автоматическая генерация упражнений

- История ваших достижений

#### 🎯 **Мотивационная система:**

- Зарабатывайте баллы за полезные привычки

- Отслеживайте прогресс в удобном формате

- Получайте награды за регулярность  


### 🛠 **Технологии под капотом**

#### **Основной стек:**

- Python 3.10+ - ядро бота

- Aiogram 3 - работа с Telegram API

- SQLite - хранение данных пользователей

- APScheduler - напоминания и планирование

#### **Дополнительно:**

- FSM (машина состояний) для удобных диалогов

- Асинхронная архитектура

- Система баллов и достижений


### ⚙️ Конфигурация

#### Файл окружения (.env):
Создайте файл `.env` в корне проекта с следующим содержимым:


# Обязательные параметры
TOKEN="7686217589:AAGZzC-XBXVuUseVS2d1b8..."  # Токен бота от @BotFather

# Настройки PostgreSQL
```
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_pass
POSTGRES_DB=db_name
POSTGRES_HOST=db  # Для Docker используйте имя сервиса
POSTGRES_PORT=5432
```

### **🚀 Быстрый старт**

1. Получите токен бота у @BotFather и склонируйте репозиторий
```
git clone git@github.com/PhosFactum/HabitQuest.git

```
2. Установите зависимости:
```
pip install -r requirements.txt
```
3. Создайте файл .env с вашим токеном в корне:
```
TOKEN=ваш_токен_здесь
```
4. Запустите бота:
```
python -m bot.py
```

### 🐳 Быстрый старт с Docker:
# 1. Склонируйте репозиторий
```
git clone git@github.com/PhosFactum/HabitQuest.git
```

# 2. Запустите бота
```
docker-compose up -d --build
```

### 💡 **Бот полностью готов к использованию сразу после запуска!**
