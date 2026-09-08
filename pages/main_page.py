from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class MainPage(BasePage):
    HEADER_LOCATOR = (By.CSS_SELECTOR, "[data-test-id='header']")
    HEADER_FALLBACK = (By.TAG_NAME, "header")

    SEARCH_INPUT_LOCATOR = (
        By.XPATH,
        "//input[@placeholder='Фильмы, сериалы, персоны']",
    )
    SEARCH_INPUT_FALLBACK = (By.CSS_SELECTOR, "input[type='search']")

    # Обновлённые локаторы для кнопки профиля (с учётом изменений верстки)
    PROFILE_BUTTON_LOCATOR = (
        By.CSS_SELECTOR,
        "button[aria-label='Меню профиля'], button[data-testid='user-avatar'],"
        " button[data-tid='user-avatar']",
    )
    PROFILE_BUTTON_FALLBACK = (
        By.CSS_SELECTOR,
        "img[alt='Аватар пользователя'], .user-avatar,"
        " [data-testid='profile-icon']",
    )

    BANNER_LOCATOR = (
        By.XPATH,
        "//div[@role='region' and @aria-label='Промо']",
    )
    BANNER_FALLBACK = (By.XPATH, "//h2[contains(text(), 'Популярные фильмы')]")
    BANNER_LINK_LOCATOR = (
        By.XPATH,
        "//a[contains(@href, 'hd.kinopoisk.ru/film')]",
    )

    def is_header_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.HEADER_LOCATOR)
            )
            return True
        except Exception:
            try:
                self.wait.until(
                    EC.visibility_of_element_located(self.HEADER_FALLBACK)
                )
                return True
            except Exception:
                return False

    def is_search_input_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.SEARCH_INPUT_LOCATOR)
            )
            return True
        except Exception:
            try:
                self.wait.until(
                    EC.visibility_of_element_located(
                        self.SEARCH_INPUT_FALLBACK
                    )
                )
                return True
            except Exception:
                return False

    def is_profile_button_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.PROFILE_BUTTON_LOCATOR)
            )
            return True
        except Exception:
            try:
                self.wait.until(
                    EC.visibility_of_element_located(
                        self.PROFILE_BUTTON_FALLBACK
                    )
                )
                return True
            except Exception:
                return False

    def is_banner_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.BANNER_LOCATOR)
            )
            return True
        except Exception:
            try:
                self.wait.until(
                    EC.visibility_of_element_located(self.BANNER_FALLBACK)
                )
                return True
            except Exception:
                return False

    def click_banner_movie(self) -> bool:
        if not self.is_banner_visible():
            return False
        try:
            link = self.wait.until(
                EC.element_to_be_clickable(self.BANNER_LINK_LOCATOR)
            )
            if self._js_click(link):
                return True
            link.click()
            return True
        except Exception:
            return False
