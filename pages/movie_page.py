from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class MoviePage(BasePage):
    # Разделяем селекторы. Selenium не умеет искать по
    # двум разным CSS через запятую в одном кортеже.
    POSTER_SRC_PART_1 = "posters"
    POSTER_SRC_PART_2 = "avatars.mds.yandex.net"

    # Ищем все img, где src содержит хотя бы одну из подстрок
    POSTER_CANDIDATES_LOCATOR = (By.TAG_NAME, "img")

    WATCH_LATER_BTN_INACTIVE = (
        By.CSS_SELECTOR,
        'button[title="Буду смотреть"][aria-pressed="false"]',
    )
    WATCH_LATER_BTN_ACTIVE = (
        By.CSS_SELECTOR,
        'button[title="В планах"][aria-pressed="true"]',
    )
    WATCH_BUTTON = (By.CSS_SELECTOR, 'a[data-testid*="Watch"]')

    # Более надежный локатор для заголовка
    # (убираем зависимость от классов .styles_...)
    MOVIE_TITLE_HEADER = (
        By.XPATH,
        "//h1[contains(@class, 'title') or contains(@class, 'movie-title')]",
    )

    def __init__(self, driver, base_url=None):
        super().__init__(driver, base_url)

    def open(self, url: str):
        """Открывает страницу фильма и ждет загрузки заголовка."""
        if not url:
            raise ValueError("Для MoviePage необходимо передать URL фильма")

        # Используем базовый open из BasePage
        super().open(url)

        # Ждем появления заголовка.
        # Если не появится за 15 сек — тест упадет сразу, без лишних циклов.
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.MOVIE_TITLE_HEADER)
            )
            print("✅ Страница фильма загружена, заголовок виден.")
        except Exception as e:
            print(
                f"❌ Не удалось загрузить страницу "
                f"фильма или найти заголовок: {e}"
            )
            raise

    def _is_poster_loaded(self, element):
        """
        Кастомное условие:
        элемент должен быть видимым И иметь нормальные размеры.
        """
        if not element.is_displayed():
            return False

        try:
            width = int(element.get_attribute("naturalWidth") or 0)
            height = int(element.get_attribute("naturalHeight") or 0)

            # Критерии "нормального" постера
            return width >= 300 and height >= 400
        except Exception:
            return False

    def is_poster_visible(self, timeout=15):
        """
        Ждет появления постера с нормальными размерами.
        Использует стандартный WebDriverWait вместо while+sleep.
        """
        print(
            f"⏳ Ждем загрузки качественного постера (макс {timeout} сек)..."
        )

        try:
            # Создаем временный wait специально для этой сложной проверки
            temp_wait = WebDriverWait(self.driver, timeout, poll_frequency=0.5)

            # Логика: найти все картинки, отфильтровать те,
            # у которых в src есть нужные части,
            # и проверить их размеры.
            def find_valid_poster(driver):
                candidates = driver.find_elements(
                    *self.POSTER_CANDIDATES_LOCATOR
                )
                for img in candidates:
                    src = img.get_attribute("src") or ""
                    if (
                        self.POSTER_SRC_PART_1 in src
                        or self.POSTER_SRC_PART_2 in src
                    ):
                        if self._is_poster_loaded(img):
                            return img
                return False

            poster_img = temp_wait.until(find_valid_poster)
            print(f"✅ Постер найден и загружен! Размеры: {poster_img.size}")
            return True

        except Exception as e:
            print(
                f"❌ Не удалось найти подходящий постер за {timeout} сек."
                f" Ошибка: {e}"
            )
            return False

    # Методы для кнопок (оставь свои реализации, они ок,
    # если используют self.wait)
    # def click_watch_later(self): ...
    # def verify_watch_later_state_changed(self): ...
    # def get_title(self): ...
