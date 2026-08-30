from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class SearchPage(BasePage):
    # Поле поиска и кнопка (как было ранее)
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[role="combobox"][placeholder*="Фильмы"]')
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"][aria-label="Найти"]')

    # Вкладки
    ALL_RESULTS_TAB = (By.CSS_SELECTOR, 'button[id="all"][role="tab"]')
    ONLINE_CINEMA_TAB = (By.CSS_SELECTOR, 'button[id="online"][role="tab"]')
    # Альтернатива по data-tid (если в проекте это предпочтительный способ)
    # ONLINE_CINEMA_TAB = (By.CSS_SELECTOR, 'button[data-tid="2ad66cc9"]')

    RESULT_LIST = (By.CLASS_NAME, "search-results")
    FIRST_RESULT = (By.CSS_SELECTOR, ".search-results .result:first-child")

    @step("Нажать на вкладку «Все результаты»")
    def click_all_results_tab(self):
        wait = WebDriverWait(self.driver, 10)
        tab = wait.until(EC.element_to_be_clickable(self.ALL_RESULTS_TAB))
        tab.click()

    @step("Нажать на вкладку «Онлайн‑кинотеатр»")
    def click_online_cinema_tab(self):
        wait = WebDriverWait(self.driver, 10)
        tab = wait.until(EC.element_to_be_clickable(self.ONLINE_CINEMA_TAB))
        tab.click()

    @step("Вкладка «Все результаты» должна быть активной")
    def verify_all_results_tab_active(self):
        self._verify_tab_active(self.ALL_RESULTS_TAB)

    @step("Вкладка «Онлайн‑кинотеатр» должна быть активной")
    def verify_online_cinema_tab_active(self):
        self._verify_tab_active(self.ONLINE_CINEMA_TAB)

    def _verify_tab_active(self, locator):
        wait = WebDriverWait(self.driver, 10)
        tab = wait.until(EC.visibility_of_element_located(locator))
        assert tab.get_attribute("aria-selected") == "true", "Вкладка не активна"

    # Остальные методы (search, is_results_visible, click_first_result) остаются без изменений
    @step("Выполнение поиска по запросу \"{query}\"")
    def search(self, query: str):
        wait = WebDriverWait(self.driver, 10)
        input_field = wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        input_field.clear()
        input_field.send_keys(query)
        btn = wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        btn.click()

    @step("Результаты поиска должны быть видны")
    def is_results_visible(self):
        wait = WebDriverWait(self.driver, 10)
        results = wait.until(EC.visibility_of_element_located(self.RESULT_LIST))
        assert results.is_displayed(), "Список результатов не появился"

    @step("Перейти к первому результату поиска")
    def click_first_result(self):
        wait = WebDriverWait(self.driver, 10)
        first_item = wait.until(EC.element_to_be_clickable(self.FIRST_RESULT))
        first_item.click()
