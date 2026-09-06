import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.kinopoisk_api import KinopoiskAPI

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import allure


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для API клиента. Живёт всю сессию."""
    return KinopoiskAPI()


@pytest.fixture(scope="function")
def driver():
    """Фикстура для браузера. Создаётся для каждого теста."""
    options = webdriver.ChromeOptions()

    # 1. Headless режим для CI
    is_ci = os.getenv("CI") == "true"
    if is_ci:
        options.add_argument("--headless=new")

    # 2. Стандартные флаги для стабильности
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # 3. АНТИДЕКТ БОТОВ — РАСКОММЕНТИРОВАНО (критично для Кинопоиска!)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Скрываем признак webdriver от JS-проверок сайта
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    yield driver

    try:
        driver.quit()
    except Exception:
        pass


def pytest_configure(config):
    config.addinivalue_line("markers", "ui: Mark test as UI test")
    config.addinivalue_line("markers", "api: Mark test as API test")


def pytest_collection_modifyitems(config, items):
    pass
