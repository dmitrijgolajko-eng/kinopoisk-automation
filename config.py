import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env, лежащего в корне проекта
load_dotenv()

# Базовые URL
BASE_URL = os.getenv("BASE_URL", "https://www.kinopoisk.ru")
API_URL = os.getenv("API_URL", "https://api.kinopoisk.dev")

# Учетные данные
KP_LOGIN = os.getenv("KP_LOGIN")
KP_PASSWORD = os.getenv("KP_PASSWORD")

# Словарь для случаев, когда удобнее передавать данные одной структурой
KP_CREDENTIALS = {
    "login": KP_LOGIN,
    "password": KP_PASSWORD
}

# API ключи
API_KEY = os.getenv("API_KEY")

# Таймауты
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 20

# Проверка на наличие критичных данных при старте (опционально, но полезно)
if not KP_LOGIN or not KP_PASSWORD:
    raise ValueError(
        "❌ Критическая ошибка конфигурации!\n"
        "Не найдены переменные KP_LOGIN или KP_PASSWORD в файле .env.\n"
        "Создайте файл .env в корне проекта."
    )
