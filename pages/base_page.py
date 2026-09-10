from typing import List, Optional, Tuple  # Добавляем импорт Tuple

from selenium.common import StaleElementReferenceException, WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, base_url: Optional[str] = None):
        self.driver: WebDriver = driver
        self.base_url: Optional[str] = base_url
        self.wait: WebDriverWait = WebDriverWait(
            driver, 15, poll_frequency=0.5
        )

    def open(self, url: Optional[str] = None) -> None:
        # Явно определяем целевой URL:
        # приоритет у переданного url, иначе base_url
        target = url or self.base_url

        # Проверка на None или пустую строку
        if not target:
            raise ValueError(
                "Не удалось определить URL для перехода: "
                "аргумент url не передан и атрибут base_url не установлен."
            )

        self.driver.get(target)

    def _js_click(self, element: WebElement) -> bool:
        """Выполняет клик через JavaScript. Возвращает True при успехе."""
        if element is None:
            return False
        try:
            self.driver.execute_script("arguments.click();", element)
            return True
        except WebDriverException:
            return False

    def close_all_overlays(self) -> bool:
        """
        Закрывает модальные окна, баннеры и оверлеи.
        Возвращает True, если было закрыто хотя бы одно окно.
        """
        closed_any: bool = False

        overlay_selectors: List[Tuple[By, str]] = [
            (By.CSS_SELECTOR, "button[aria-label='Закрыть']"),
            (By.CSS_SELECTOR, "button[aria-label='Close']"),
            (By.CSS_SELECTOR, "[data-testid='close-modal']"),
            (By.CSS_SELECTOR, "[data-testid='close-carousel']"),
            (By.CSS_SELECTOR, "[data-test-id='close']"),
            (By.CSS_SELECTOR, ".close-icon"),
            (By.CSS_SELECTOR, ".close-btn"),
            (By.CSS_SELECTOR, "div.overlay"),
            (By.CSS_SELECTOR, "div.modal-overlay"),
            (By.CSS_SELECTOR, "[data-testid='overlay']"),
            (By.CSS_SELECTOR, "[data-test-id='auth-banner-close']"),
            (By.CSS_SELECTOR, "[data-test-id='overlay-close']"),
        ]

        for by, selector in overlay_selectors:
            try:
                # Ищем все элементы по селектору
                elements: List[WebElement] = self.driver.find_elements(
                    by, selector
                )
            except WebDriverException:
                # Если ошибка при поиске (редко,
                # но бывает при краше страницы), пропускаем селектор
                continue

            for el in elements:
                try:
                    # Проверяем видимость. Это место,
                    # где чаще всего возникает StaleElementReferenceException
                    if el.is_displayed():
                        if self._js_click(el):
                            closed_any = True
                except (WebDriverException, StaleElementReferenceException):
                    # Элемент мог исчезнуть или стать невалидным,
                    # просто пропускаем его
                    continue

        return closed_any
