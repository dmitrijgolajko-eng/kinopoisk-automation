import os

# 1. ЧЕТКО объявляем переменные (имена должны быть идентичны тем, что используются ниже)
KP_BASE_URL = os.getenv("KP_BASE_URL")
KP_API_URL = os.getenv("KP_API_URL")
KP_API_KEY = os.getenv("KP_API_KEY")  # Если нужен ключ
KP_LOGIN = os.getenv("KP_LOGIN")  # Если нужен логин
KP_PASSWORD = os.getenv("KP_PASSWORD")  # Если нужен пароль


# 2. Функция валидации
def validate_config():
    # ВАЖНО: Ключи словаря - это просто названия для отчета.
    # Значения справа от двоеточия - это ТЕ САМЫЕ переменные, которые мы объявили выше.
    required_vars = {
        "KP_BASE_URL": KP_BASE_URL,
        "KP_API_URL": KP_API_URL,
        # Раскомментируйте строки ниже, только если эти переменные реально нужны и заданы
        # "KP_API_KEY": KP_API_KEY,
        # "KP_LOGIN": KP_LOGIN,
        # "KP_PASSWORD": KP_PASSWORD,
    }

    missing_vars = [name for name, value in required_vars.items() if not value]

    if missing_vars:
        error_message = f"❌ Критическая ошибка конфигурации! Не найдены: {', '.join(missing_vars)}"
        print(error_message)
        raise ValueError(error_message)

    print("✅ Конфигурация успешно проверена!")


# 3. ВЫЗЫВАЕМ валидацию ТОЛЬКО ПОСЛЕ объявления переменных
validate_config()
