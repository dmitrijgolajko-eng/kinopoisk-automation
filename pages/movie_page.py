from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage

class MoviePage(BasePage):
    # Улучшенные локаторы
    WATCH_LATER_BTN_INACTIVE = (By.CSS_SELECTOR, 'button[title="Буду смотреть"][aria-pressed="false"]')
    WATCH_LATER_BTN_ACTIVE = (By.CSS_SELECTOR, 'button[title="В планах"][aria-pressed="true"]')
    WATCH_BUTTON = (By.CSS_SELECTOR, 'a[data-test-id*="Watch"]')  # частичное совпадение
    MOVIE_TITLE = (By.XPATH, '//h1[contains(text(), "Бойцовский клуб")]')  # обычно заголовок фильма — это h1

    @step("Нажать кнопку «Буду смотреть»")
    def click_watch_later(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable(self.WATCH_LATER_BTN_INACTIVE))
        btn.click()

    @step("Кнопка «Буду смотреть» должна переключиться в состояние «В планах»")
    def verify_watch_later_state_changed(self):
        wait = WebDriverWait(self.driver, 10)
        active_btn = wait.until(EC.presence_of_element_located(self.WATCH_LATER_BTN_ACTIVE))
        assert active_btn.is_displayed(), "Кнопка не переключилась в состояние «В планах»"

    @step("Нажать кнопку «Смотреть»")
    def click_watch_button(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable(self.WATCH_BUTTON))
        btn.click()

    @step("Заголовок фильма должен содержать «{title}»")
    def verify_movie_title(self, title: str):
        wait = WebDriverWait(self.driver, 10)
        locator = (By.XPATH, f'//h1[contains(text(), "{title}")]')
        element = wait.until(EC.visibility_of_element_located(locator))
        assert title in element.text, f"Заголовок не содержит '{title}'"
