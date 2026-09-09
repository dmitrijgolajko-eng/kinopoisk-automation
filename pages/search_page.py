from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class SearchPage(BasePage):
    # Локаторы
    SEARCH_INPUT_LOCATOR = (
        By.CSS_SELECTOR,
        'input[placeholder="Фильмы, сериалы, персоны"]',
    )
    # Локатор карточки результата (первая карточка в выдаче)
    FIRST_RESULT_LOCATOR = (
        By.CSS_SELECTOR,
        'div[data-test-id="movie-list-item"]',
    )

    # Локаторы для подсказок (используются только для проверки наличия,
    # не для клика)
    SUGGESTION_CONTAINER_LOCATOR = (
        By.CSS_SELECTOR,
        'div[data-tid="suggest-list"]',
    )
    SUGGESTION_LINK_LOCATOR = (By.CSS_SELECTOR, 'a[href*="/film/"]')

    def search_movie(self, query: str):
        print(f"🎬 Начинаем поиск: '{query}'")

        # 1. Находим поле ввода
        input_field = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT_LOCATOR)
        )

        # 2. Вводим текст
        input_field.clear()
        input_field.send_keys(query)
        print(f"✅ Текст '{query}' введен.")

        # 3. ВАЖНО: Не пытаемся кликать по подсказкам.
        # Клик по подсказкам в Кинопоиске часто нестабилен
        # из-за JS-обработчиков и анимаций.
        # Нажатие Enter — это стандартное поведение пользователя,
        # которое гарантированно
        # инициирует поиск и открывает страницу выдачи (/new-search/).
        print("🖱️ Нажимаем Enter для запуска поиска...")
        input_field.send_keys(Keys.ENTER)

        # 4. Ждем результатов выдачи
        self.wait_for_results()

    def wait_for_results(self):
        """Ожидание загрузки результатов поиска"""
        print("⏳ Ожидаем появления и видимости результатов поиска...")

        try:
            # Ждем ВИДИМОСТИ элемента (а не просто наличия в DOM).
            # visibility_of_element_located гарантирует,
            # что элемент имеет размер > 0
            # и не скрыт (display: none / opacity: 0).
            result_element = self.wait.until(
                EC.visibility_of_element_located(self.FIRST_RESULT_LOCATOR)
            )

            # Дополнительная страховка: ждем,
            # пока внутри элемента появится текст.
            # Это гарантирует, что карточка не просто
            # «пустой контейнер», а реально загружена.
            self.wait.until(lambda d: len(result_element.text.strip()) > 0)

            print(f"✅ Найдено: {result_element.text[:50]}...")

        except TimeoutException:
            # Если основной локатор не сработал,
            # пробуем найти любой элемент выдачи.
            # Часто структура меняется,
            # и data-tid может быть на родителе или иметь другой суффикс.
            print(
                "⚠️ Основной локатор не сработал, ищем любой элемент выдачи..."
            )
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-tid*="search-result"]')
                )
            )
            print("✅ Элементы выдачи найдены (альтернативный селектор)")

    def get_search_results_count(self):
        """Возвращает количество найденных результатов"""
        try:
            # Исправляем локатор на актуальный
            results = self.driver.find_elements(
                By.CSS_SELECTOR, 'div[data-test-id="movie-list-item"]'
            )
            return len(results)
        except Exception as e:
            print(f"Ошибка при подсчете результатов: {e}")
            return 0
