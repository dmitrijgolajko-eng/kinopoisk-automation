from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from allure import step

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    @step("Открытие страницы")
    def open(self, url):
        self.driver.get(url)

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
