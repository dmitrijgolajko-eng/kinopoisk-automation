import os

KP_BASE_URL = "https://kinopoisk.ru"
KP_API_URL = os.getenv("KP_API_URL")
KP_API_KEY = os.getenv("KP_API_KEY")
KP_LOGIN = os.getenv("KP_LOGIN")
KP_PASSWORD = os.getenv("KP_PASSWORD")
KP_COOKIES = [
    {"name": "yandexuid", "value": "1042763991788677924", "domain": ".yandex.ru", "path": "/"},
    {"name": "ya_sess_id", "value": "3:1788675445.5.0.1788675440950:2sbeqA:d7c6.1.2:1|661376346.-1.20002.3:1788675440|30:12165277.999146.Zb_j3oxYtIXDQRA2ILlIICAjSRM", "domain": ".kinopoisk.ru", "path": "/"},
    {"name": "Session_id", "value": "3:1788675440.5.0.1788675440950:2sbeqA:d7c6.1.2:1|661376346.-1.20002.3:1788675440|3:12165268.419107.xmGBpLv3x83TkKOst0nhMrGToqU", "domain": ".kinopoisk.ru", "path": "/"}
]

def validate_config():
    required_vars = {
        "KP_BASE_URL": KP_BASE_URL,
        # Если API не используется в UI-тестах, можно убрать эти строки
        # "KP_API_URL": KP_API_URL,
        # "KP_API_KEY": KP_API_KEY,
        "KP_LOGIN": KP_LOGIN,
        "KP_PASSWORD": KP_PASSWORD,
    }

    missing_vars = [name for name, value in required_vars.items() if not value]

    if missing_vars:
        error_message = f"❌ Критическая ошибка конфигурации! Не найдены: {', '.join(missing_vars)}"
        print(error_message)
        raise ValueError(error_message)

    print("✅ Конфигурация успешно проверена!")

validate_config()

