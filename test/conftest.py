import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Теперь эти импорты должны сработать
from api.kinopoisk_api import KinopoiskAPI

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api.kinopoisk_api import KinopoiskAPI
import allure


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для API клиента. Живет всю сессию."""
    return KinopoiskAPI()


@pytest.fixture(scope="function")
def driver():
    """Фикстура для браузера. Создается для каждого теста."""
    options = webdriver.ChromeOptions()

    # 1. HEADLESS РЕЖИМ (Обязательно для CI)
    # Если переменная CI=true или мы на Linux сервере без GUI, включаем headless
    is_ci = os.getenv("CI") == "true" or os.name != 'nt'
    if is_ci or "--headless" in os.environ.get("PYTEST_ARGS", ""):
        options.add_argument("--headless=new")

    # 2. Стандартные флаги для стабильности в Docker/CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # Для старых версий Chrome на Linux
    options.add_argument("--window-size=1920,1080")  # Важно для headless: задаем размер окна явно

    # 3. Флаги для отладки (опционально, можно убрать в продакшен)
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # ВАЖНО: Убираем implicitly_wait!
    # Используем явные ожидания (WebDriverWait) внутри PageObject.
    # Это ускоряет тесты и делает их стабильнее.

    yield driver

    # Корректное завершение
    try:
        driver.quit()
    except Exception:
        # Если драйвер уже закрыт (например, краш браузера), игнорируем ошибку
        pass


def pytest_configure(config):
    config.addinivalue_line("markers", "ui: Mark test as UI test")
    config.addinivalue_line("markers", "api: Mark test as API test")


def pytest_collection_modifyitems(config, items):
    """
    Опционально: Можно добавить логику здесь.
    Например, автоматически добавлять метку 'ui' всем тестам из папки tests/ui/
    """
    pass
