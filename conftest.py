import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from api.kinopoisk_api import KinopoiskAPI

load_dotenv(override=True)


@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)

    ya_sess_id = os.getenv("KP_COOKIE_YA_SESS_ID")
    yandex_login = os.getenv("KP_COOKIE_YANDEX_LOGIN")
    yandex_uid = os.getenv("KP_COOKIE_YANDEXUID")
    yuidss = os.getenv("KP_COOKIE_YUIDSS")

    cookies_to_add = []

    if ya_sess_id:
        cookies_to_add.append(
            {
                "name": "ya_sess_id",
                "value": ya_sess_id,
                "domain": ".kinopoisk.ru",
                "path": "/",
            }
        )
    if yandex_login:
        cookies_to_add.append(
            {
                "name": "yandex_login",
                "value": yandex_login,
                "domain": ".kinopoisk.ru",
                "path": "/",
            }
        )
    if yandex_uid:
        cookies_to_add.append(
            {
                "name": "yandex_uid",
                "value": yandex_uid,
                "domain": ".kinopoisk.ru",
                "path": "/",
            }
        )
    if yuidss:
        cookies_to_add.append(
            {
                "name": "yuidss",
                "value": yuidss,
                "domain": ".kinopoisk.ru",
                "path": "/",
            }
        )

    if cookies_to_add:
        print(
            f"🍪 Найдено {len(cookies_to_add)} куки. Начинаем авторизацию..."
        )
        try:
            driver.get("https://www.kinopoisk.ru")
            for cookie in cookies_to_add:
                driver.add_cookie(cookie)
                print(f"   ✅ Добавлена кука: {cookie['name']}")
            driver.refresh()
            print("✅ Авторизация успешна. Страница обновлена.")
        except Exception as e:
            print(f"❌ Ошибка установки куки: {e}")
    else:
        print(
            "⚠️ ВНИМАНИЕ: Ни одна из переменных KP_COOKIE_* не найдена в ENV!"
        )
        print(
            "⚠️ Тест будет выполняться от имени гостя."
            " Кнопка профиля может быть не видна."
        )
        print(
            "💡 Совет: Проверьте Run Configuration в "
            "PyCharm и вставьте значения."
        )

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def api_client():
    # Получаем параметры из переменных окружения
    base_url = os.getenv("KP_API_URL", "https://api.kinopoisk.dev")
    api_version = os.getenv("KP_API_VERSION", "v1.4")
    api_key = os.getenv("KP_API_KEY")

    if not api_key:
        print("⚠️ ВНИМАНИЕ: Переменная KP_API_KEY не найдена в ENV!")
        print("💡 Совет: Добавьте KP_API_KEY в конфигурацию запуска.")

    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

    return KinopoiskAPI(
        base_url=base_url, api_version=api_version, headers=headers
    )
