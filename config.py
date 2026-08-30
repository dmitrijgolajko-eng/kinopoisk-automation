import os

# Базовые URL
BASE_URL = os.getenv("KP_BASE_URL", "https://www.kinopoisk.ru")
API_URL = os.getenv("KP_API_URL", "https://api.kinopoisk.dev")

# Учетные данные
KP_LOGIN = os.getenv("KP_LOGIN")
KP_PASSWORD = os.getenv("KP_PASSWORD")

# Словарь для учетных данных
KP_CREDENTIALS = {
    "login": KP_LOGIN,
    "password": KP_PASSWORD
}

# API ключи
API_KEY = os.getenv("KP_API_KEY")

# Таймауты
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 20


# Проверка наличия всех необходимых переменных
def validate_config():
    required_vars = {
        "KP_BASE_URL": BASE_URL,
        "KP_API_URL": API_URL,
        "KP_LOGIN": KP_LOGIN,
        "KP_PASSWORD": KP_PASSWORD,
        "KP_API_KEY": API_KEY
    }

    missing_vars = [name for name, value in required_vars.items() if not value]

    if missing_vars:
        raise ValueError(
            "❌ Критическая ошибка конфигурации!\n"
            f"Не найдены следующие переменные окружения:\n"
            f"{'\n'.join(missing_vars)}\n"
            "Установите переменные окружения в системе."
        )


# Выполняем проверку при импорте файла
validate_config()
