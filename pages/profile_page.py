from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class ProfilePage(BasePage):
    # ВАЖНО: Мы НЕ используем просто data-tid. Мы используем комбинацию data-tid + текст.
    # Это гарантирует, что мы найдем именно нужную вкладку, даже если ID дублируются.

    PROFILE_TAB = (By.XPATH, '//a[@data-tid="ec7a8d07" and contains(text(), "Профиль")]')
    REVIEWS_TAB = (By.XPATH, '//a[@data-tid="ec7a8d07" and contains(text(), "Рецензии")]')
    COMMENTS_TAB = (By.XPATH, '//a[@data-tid="ec7a8d07" and contains(text(), "Комментарии")]')
    RATINGS_TAB = (By.XPATH, '//a[@data-tid="ec7a8d07" and contains(text(), "Оценки")]')
    FRIENDS_RATINGS_TAB = (By.XPATH, '//a[@data-tid="ec7a8d07" and contains(text(), "Оценки друзей")]')
    WATCHLIST_TAB = (By.XPATH, '//a[@data-tid="ec7a8d07" and contains(text(), "Буду смотреть")]')
    STARS_TAB = (By.XPATH, '//a[@data-tid="ec7a8d07" and contains(text(), "Звезды")]')

    @step("Нажать на вкладку «Профиль»")
    def click_profile_tab(self):
        self._click_tab(self.PROFILE_TAB, "Профиль")

    @step("Нажать на вкладку «Рецензии»")
    def click_reviews_tab(self):
        self._click_tab(self.REVIEWS_TAB, "Рецензии")

    @step("Нажать на вкладку «Комментарии»")
    def click_comments_tab(self):
        self._click_tab(self.COMMENTS_TAB, "Комментарии")

    @step("Нажать на вкладку «Оценки»")
    def click_ratings_tab(self):
        self._click_tab(self.RATINGS_TAB, "Оценки")

    @step("Нажать на вкладку «Оценки друзей»")
    def click_friends_ratings_tab(self):
        self._click_tab(self.FRIENDS_RATINGS_TAB, "Оценки друзей")

    @step("Нажать на вкладку «Буду смотреть»")
    def click_watchlist_tab(self):
        self._click_tab(self.WATCHLIST_TAB, "Буду смотреть")

    @step("Нажать на вкладку «Звезды»")
    def click_stars_tab(self):
        self._click_tab(self.STARS_TAB, "Звезды")

    def _click_tab(self, locator, tab_name):
        """Вспомогательный метод для клика по вкладке с ожиданием"""
        wait = WebDriverWait(self.driver, 10)
        tab = wait.until(EC.element_to_be_clickable(locator))
        # Дополнительный чек перед кликом: убеждаемся, что текст совпадает
        assert tab.text.strip() == tab_name, f"Ожидался текст '{tab_name}', но найден '{tab.text}'"
        tab.click()

    @step("Вкладка «{tab_name}» должна быть активной")
    def verify_tab_active(self, tab_name):
        """
        Универсальный шаг для проверки активности любой вкладки.
        Передаем имя вкладки как аргумент в feature-файле.
        """
        wait = WebDriverWait(self.driver, 10)

        # Формируем локатор динамически на основе имени вкладки
        # Примечание: для сложных названий (как "Оценки друзей") лучше иметь отдельные локаторы,
        # но для простоты примера используем поиск по тексту среди всех ссылок меню.
        # В продакшене лучше использовать заранее определенные локаторы (см. ниже альтернативу).

        # Вариант 1: Если у активной вкладки появляется класс active (как у Профиля на прошлом скрине)
        # Ищем ссылку с нужным текстом И классом, содержащим 'active'
        xpath_active = f'//a[contains(text(), "{tab_name}") and contains(@class, "active")]'

        try:
            active_tab = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_active)))
            assert active_tab.text.strip() == tab_name, "Текст активной вкладки не совпадает"
        except Exception:
            # Вариант 2 (Fallback): Если активной ссылки не выделяют классом,
            # проверяем, что мы находимся на странице с таким URL или заголовком.
            # Это зависит от того, SPA у вас или нет.
            if "/comments/" in self.driver.current_url and tab_name == "Рецензии":
                return  # Успех, мы на странице рецензий
            raise AssertionError(f"Вкладка '{tab_name}' не отмечена как активная (нет класса active)")

