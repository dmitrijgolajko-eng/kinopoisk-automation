import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api.kinopoisk_api import KinopoiskAPI
from pages.base_page import BasePage
import allure

@pytest.fixture(scope="session")
def api_client():
    return KinopoiskAPI()

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def base_page(driver):
    return BasePage(driver)

def pytest_configure(config):
    config.addinivalue_line("markers", "ui: Mark test as UI test")
    config.addinivalue_line("markers", "api: Mark test as API test")

    # Allure environment лучше задавать не здесь, а через allure-properties или env vars
    # allure.environment(browser="Chrome", platform="Windows")

def pytest_collection_modifyitems(config, items):
    # Опционально: можно добавить логику фильтрации или сортировки тестов
    pass
