import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Базовые URL
BASE_URL = os.getenv("KP_BASE_URL", "https://www.kinopoisk.ru")
API_URL = os.getenv("KP_API_URL", "https://api.kinopoisk.dev")

# Учетные данные
KP_LOGIN = os.getenv("KP_LOGIN")
KP_PASSWORD = os.getenv("KP_PASSWORD")

# API ключи
API_KEY = os.getenv("KP_API_KEY")

# Таймауты (в секундах)
TIMEOUTS = {
    "implicit": int(os.getenv("KP_IMPLICIT_WAIT", 10)),
    "explicit": int(os.getenv("KP_EXPLICIT_WAIT", 20))
}

# Словарь для учетных данных
KP_CREDENTIALS = {
    "login": KP_LOGIN,
    "password": KP_PASSWORD
}

def validate_config():
    required_vars = {
        "KP_LOGIN": KP_LOGIN,
        "KP_PASSWORD": KP_PASSWORD,
        "KP_API_KEY": API_KEY
    }

    missing_vars = [name for name, value in required_vars.items() if not value]

    if missing_vars:
        error_message = (
            "❌ Критическая ошибка конфигурации!\n"
            f"Не найдены следующие обязательные переменные окружения:\n"
            f"{'\n'.join(missing_vars)}\n"
            "Установите переменные окружения в системе."
        )
        logger.error(error_message)
        raise ValueError(error_message)

    logger.info("Конфигурация успешно проверена")

# Выполняем проверку при импорте файла
validate_config()

