from behave import step
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchPage(BasePage):
    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-button")
    RESULT_LIST = (By.CLASS_NAME, "search-results")
    FIRST_RESULT = (By.CSS_SELECTOR, ".search-results .result:first-child")

    @step("Выполнение поиска")
    def search(self, query):
        self.input_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    @step("Проверка результатов поиска")
    def is_results_visible(self):
        return self.wait_for_element(self.RESULT_LIST).is_displayed()

    @step("Переход к первому результату")
    def click_first_result(self):
        self.click(self.FIRST_RESULT)
