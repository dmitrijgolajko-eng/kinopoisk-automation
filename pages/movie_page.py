from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class MoviePage(BasePage):
    # Универсальные локаторы (без привязки к конкретному фильму)
    WATCH_LATER_BTN_INACTIVE = (By.CSS_SELECTOR, 'button[title="Буду смотреть"][aria-pressed="false"]')
    WATCH_LATER_BTN_ACTIVE = (By.CSS_SELECTOR, 'button[title="В планах"][aria-pressed="true"]')

    # Уточненный локатор кнопки "Смотреть".
    # Если у кнопки есть уникальный data-testid, используйте точное совпадение вместо *=.
    # Пример: 'a[data-testid="movie-watch-button"]'
    WATCH_BUTTON = (By.CSS_SELECTOR, 'a[data-testid*="Watch"]')

    # Универсальный локатор заголовка (без названия фильма)
    MOVIE_TITLE_HEADER = (By.CSS_SELECTOR, 'h1.movie-title, h1[class*="title"]')

    def __init__(self, driver):
        super().__init__(driver)
        # Инициализируем wait один раз в конструкторе
        self.wait = WebDriverWait(self.driver, 15)

    @step("Нажать кнопку «Буду смотреть»")
    def click_watch_later(self):
        # Используем общий wait из __init__
        btn = self.wait.until(EC.element_to_be_clickable(self.WATCH_LATER_BTN_INACTIVE))
        btn.click()

    @step("Кнопка «Буду смотреть» должна переключиться в состояние «В планах»")
    def verify_watch_later_state_changed(self):
        # Ждем появления активной кнопки.
        # Если кнопка не переключается быстро, можно добавить явную проверку исчезновения старой кнопки
        try:
            self.wait.until(EC.presence_of_element_located(self.WATCH_LATER_BTN_ACTIVE))
        except Exception:
            # Фоллбэк: проверяем, что старая кнопка больше не активна (aria-pressed="false")
            # Это повышает устойчивость теста к микро-задержкам рендера
            self.wait.until(EC.invisibility_of_element_located(self.WATCH_LATER_BTN_INACTIVE))

        active_btn = self.driver.find_element(*self.WATCH_LATER_BTN_ACTIVE)
        assert active_btn.is_displayed(), "Кнопка не переключилась в состояние «В планах»"

    @step("Нажать кнопку «Смотреть»")
    def click_watch_button(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.WATCH_BUTTON))
        btn.click()

    @step("Заголовок фильма должен содержать «{title}»")
    def verify_movie_title(self, title: str):
        # Используем универсальный локатор и ищем текст внутри него
        header = self.wait.until(EC.visibility_of_element_located(self.MOVIE_TITLE_HEADER))

        # Нормализуем текст (убираем лишние пробелы/переносы) для надежного сравнения
        header_text = header.text.strip()

        assert title in header_text, f"Заголовок '{header_text}' не содержит ожидаемого '{title}'"
