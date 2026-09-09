import os

KP_BASE_URL = "https://kinopoisk.ru"
KP_API_URL = os.getenv("KP_API_URL")
KP_API_KEY = os.getenv("KP_API_KEY")
KP_LOGIN = os.getenv("KP_LOGIN")
KP_PASSWORD = os.getenv("KP_PASSWORD")

# --- ОБНОВЛЕННЫЕ ПЕРЕМЕННЫЕ ДЛЯ КУКИ ---
# Теперь мы не используем одну общую строку KP_COOKIES.
# Вместо этого мы читаем каждую куку отдельно,
# чтобы гибко управлять ими в conftest.py
KP_COOKIE_YA_SESS_ID = os.getenv("KP_COOKIE_YA_SESS_ID")
KP_COOKIE_YANDEX_LOGIN = os.getenv("KP_COOKIE_YANDEX_LOGIN")
KP_COOKIE_YANDEXUID = os.getenv("KP_COOKIE_YANDEXUID")
KP_COOKIE_YUIDSS = os.getenv("KP_COOKIE_YUIDSS")
