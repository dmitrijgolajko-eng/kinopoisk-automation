from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url: Optional[str] = None):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 15, poll_frequency=0.5)

    def open(self, url: Optional[str] = None) -> None:
        target = url if url else self.base_url
        if not target:
            raise ValueError("URL не передан и base_url не установлен")
        self.driver.get(target)

    def _js_click(self, element) -> bool:
        if not element:
            return False
        try:
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception:
            return False

    def close_all_overlays(self) -> bool:
        """
        Закрывает модальные окна, баннеры и оверлеи Кинопоиска.
        Использует короткий таймаут (2 сек), чтобы не тормозить тест.
        """
        closed_any = False

        # Все возможные селекторы оверлеев в одном списке
        overlay_selectors = [
            # Кнопки закрытия
            (By.CSS_SELECTOR, "button[aria-label='Закрыть']"),
            (By.CSS_SELECTOR, "button[aria-label='Close']"),
            (By.CSS_SELECTOR, "[data-testid='close-modal']"),
            (By.CSS_SELECTOR, "[data-testid='close-carousel']"),
            (By.CSS_SELECTOR, "[data-test-id='close']"),
            (By.CSS_SELECTOR, ".close-icon"),
            (By.CSS_SELECTOR, ".close-btn"),
            # Оверлеи (клик по фону закрывает окно)
            (By.CSS_SELECTOR, "div.overlay"),
            (By.CSS_SELECTOR, "div.modal-overlay"),
            (By.CSS_SELECTOR, "[data-testid='overlay']"),
            # Баннер авторизации/подписки
            (By.CSS_SELECTOR, "[data-test-id='auth-banner-close']"),
            (By.CSS_SELECTOR, "[data-test-id='overlay-close']"),
        ]

        for by, selector in overlay_selectors:
            try:
                elements = self.driver.find_elements(by, selector)
                for el in elements:
                    if el.is_displayed():
                        if self._js_click(el):
                            closed_any = True
                        import time

                        time.sleep(0.3)
            except Exception:
                continue

        return closed_any
