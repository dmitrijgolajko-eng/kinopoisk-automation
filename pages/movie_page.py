# pages/movie_page.py
from .base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class MoviePage(BasePage):
    # --- СТАБИЛЬНЫЕ ЛОКАТОРЫ (НЕ зависят от классов .styles_...) ---

    # Ищем img, у которого в src есть 'posters' (основной постер)
    # ИЛИ 'avatars.mds.yandex.net' (альтернативный CDN Кинопоиска)
    POSTER_LOCATOR = (By.CSS_SELECTOR, "img[src*='posters'], img[src*='avatars.mds.yandex.net']")

    # Остальные твои локаторы оставляем без изменений
    WATCH_LATER_BTN_INACTIVE = (By.CSS_SELECTOR, 'button[title="Буду смотреть"][aria-pressed="false"]')
    WATCH_LATER_BTN_ACTIVE = (By.CSS_SELECTOR, 'button[title="В планах"][aria-pressed="true"]')
    WATCH_BUTTON = (By.CSS_SELECTOR, 'a[data-testid*="Watch"]')
    MOVIE_TITLE_HEADER = (By.CSS_SELECTOR, 'h1.movie-title, h1[class*="title"]')

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

    def open(self, url: str):
        if not url:
            raise ValueError("Для MoviePage необходимо передать URL фильма")
        super().open(url)
        # Ждем появления заголовка, чтобы убедиться, что страница фильма загружена
        self.wait.until(EC.visibility_of_element_located(self.MOVIE_TITLE_HEADER))

    # ... (оставь свои методы click_watch_later, verify_watch_later_state_changed, get_title без изменений) ...

    def _get_loaded_poster_element(self, timeout=15):
        print(f"⏳ Ищем постер и ждем его загрузки (макс {timeout} сек)...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                candidates = self.driver.find_elements(*self.POSTER_LOCATOR)

                for img in candidates:
                    width = int(img.get_attribute("naturalWidth") or 0)
                    height = int(img.get_attribute("naturalHeight") or 0)

                    # Проверяем минимальные размеры постера
                    if width >= 300 and height >= 400 and img.is_displayed():
                        print(f"✅ Постер найден! Размер: {width}x{height}px")
                        return img

                    # Если нашли маленький постер, пробуем следующий
                    print(f"⚠️ Найден постер размером {width}x{height}px, продолжаем поиск...")

                time.sleep(0.5)

            except Exception as e:
                print(f"⚠️ Ошибка при проверке постера: {e}")
                time.sleep(0.5)

        print("❌ Не удалось найти подходящий постер за отведенное время.")
        return None

    def is_poster_visible(self):
        """
        Публичный метод для теста. Возвращает True только если постер есть и загружен.
        """
        poster_img = self._get_loaded_poster_element(timeout=15)
        return poster_img is not None
