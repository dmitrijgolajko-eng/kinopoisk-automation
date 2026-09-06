# pages/search_page.py
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class SearchPage(BasePage):
    # Локатор для ссылки в выпадающем списке подсказок
    SUGGESTION_LINK_LOCATOR = (By.CSS_SELECTOR, "a[href*='/film/']")

    # Локатор для проверки финальной страницы (любой элемент фильма)
    PAGE_LOAD_CHECK_LOCATOR = (By.CSS_SELECTOR, "a[href*='/film/'], .film-title, h1")

    def _wait_for_active_input(self, timeout=10):
        """Ждет, пока поле ввода получит фокус (автофокус)"""
        print(f"⏳ Ждем автофокуса в поле поиска (макс. {timeout} сек)...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                active_elem = self.driver.switch_to.active_element
                tag = active_elem.tag_name.lower()
                input_type = active_elem.get_attribute("type")

                # Проверяем, что это input и он активен
                if tag == "input" and input_type in ["text", "search"]:
                    # Дополнительная проверка: убедимся, что он не скрыт (display: none)
                    if active_elem.is_displayed():
                        print("✅ Автофокус найден!")
                        return active_elem
            except Exception:
                pass
            time.sleep(0.3)

        raise TimeoutError("❌ Не удалось дождаться автофокуса в поле поиска. Возможно, оверлей не закрыт.")

    def search_movie(self, query: str):
        print(f"🎬 Начинаем поиск: '{query}'")

        # 1. Получаем поле ввода через автофокус
        input_field = self._wait_for_active_input()

        # 2. Вводим текст
        input_field.clear()
        input_field.send_keys(query)
        print(f"✅ Текст '{query}' введен.")

        # 3. Ждем появления списка подсказок и кликаем по первой
        print("⏳ Ждем появления выпадающего списка подсказок...")
        try:
            # Ждем кликабельной ссылки на фильм в списке
            suggestion_link = self.wait.until(EC.element_to_be_clickable(self.SUGGESTION_LINK_LOCATOR))
            print("✅ Подсказка найдена, кликаем...")
            self._js_click(suggestion_link)
        except Exception as e:
            print(f"⚠️ Список подсказок не появился или пуст. Пробуем нажать Enter...")
            # Фоллбэк: если списка нет, жмем Enter в поле ввода
            input_field.send_keys("\n")

        # 4. Ждем загрузки финальной страницы (без жесткого sleep, только по факту появления элемента)
        print("⏳ Ждем загрузки страницы фильма...")
        self.wait.until(EC.presence_of_element_located(self.PAGE_LOAD_CHECK_LOCATOR))
        print("✅ Страница фильма начала загружаться.")

    def wait_for_results(self):
        """Финальная валидация: убеждаемся, что мы на странице фильма"""
        print("🔍 Финальная проверка URL и элементов...")
        # Проверяем, что в URL есть /film/
        current_url = self.driver.current_url
        assert "/film/" in current_url, f"Ожидался URL с /film/, но получили: {current_url}"

        # Проверяем наличие элемента с ссылкой на фильм
        element = self.wait.until(EC.visibility_of_element_located(self.SUGGESTION_LINK_LOCATOR))
        href = element.get_attribute("href")
        print(f"✅ Тест пройден! Целевой URL: {href}")
        return element
