from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from allure import step

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.url = None  # Инициализируем, чтобы избежать ошибок при обращении

    @step("Открытие страницы")
    def open(self):
        if not self.url:
            raise ValueError(f"URL не задан для страницы {self.__class__.__name__}."
                             f" Определите self.url в __init__ дочернего класса.")
        self.driver.get(self.url)

    @step("Ожидание элемента")
    def wait_for_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @step("Клик по элементу")
    def click(self, locator):
        element = self.wait_for_element(locator)
        element.click()

    @step("Ввод текста")
    def input_text(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)
