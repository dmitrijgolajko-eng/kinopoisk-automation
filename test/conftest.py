import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api.kinopoisk_api import KinopoiskAPI
from pages.base_page import BasePage

@pytest.fixture(scope="session")
def api_client():
    return KinopoiskAPI()

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Раскомментировать для запуска без GUI
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def base_page(driver):
    return BasePage(driver)

# Маркер для UI тестов
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "ui: Mark test as UI test"
    )
    config.addinivalue_line(
        "markers",
        "api: Mark test as API test"
    )
