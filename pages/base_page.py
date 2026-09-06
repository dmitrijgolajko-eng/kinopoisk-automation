# pages/base_page.py

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException


class BasePage:
    def __init__(self, driver, base_url=None):
        self.driver = driver
        self.base_url = base_url          # ДОБАВЛЕНО
        self.wait = WebDriverWait(driver, 20, poll_frequency=0.5)

    def open(self, url=None):
        target = url if url else self.base_url    # ДОБАВЛЕНО: fallback на base_url
        if target:
            self.driver.get(target)

    def _js_click(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"❌ JS клик не удался: {e}")
            return False

    def close_all_overlays(self):
        closed_count = 0

        # --- ТИПА 1: Модальные окна ---
        try:
            locator = (By.CSS_SELECTOR, "button[data-tid='CloseButton']")
            btn = self.wait.until(EC.element_to_be_clickable(locator))
            if self._js_click(btn):
                self.wait.until(EC.invisibility_of_element_located(locator))
                print("✅ Закрыто верхнее модальное окно.")
                closed_count += 1
        except TimeoutException:
            pass
        except Exception as e:
            print(f"⚠️ Ошибка при закрытии верхнего окна: {e}")

        # --- ТИПА 2: Нижние sticky-баннеры ---
        try:
            banner_locator = (By.CSS_SELECTOR, "div[style*='bottom: 0'], div[style*='position: fixed']")
            banner = self.wait.until(EC.presence_of_element_located(banner_locator))
            close_btns = banner.find_elements(By.CSS_SELECTOR, "button, span, div")

            for btn in close_btns:
                label = btn.get_attribute("aria-label") or ""
                if "закрыть" in label.lower() or "close" in label.lower():
                    if self._js_click(btn):
                        print("✅ Закрыто нижнее окно авторизации.")
                        closed_count += 1
                        break

            if closed_count == 0:
                width = self.driver.execute_script("return window.innerWidth")
                height = self.driver.execute_script("return window.innerHeight")
                self.driver.execute_script(
                    f"window.document.elementFromPoint({width / 2}, {height / 4}).click();"
                )
        except TimeoutException:
            pass
        except Exception as e:
            print(f"⚠️ Ошибка при обработке нижнего баннера: {e}")

        return closed_count > 0

    def click_login_button(self):
        try:
            locator = (By.CSS_SELECTOR, "button[data-testid='loginHeaderButton']")
            btn = self.wait.until(EC.element_to_be_clickable(locator))
            if self._js_click(btn):
                print("✅ Кнопка 'Войти' нажата.")
                return True
            return False
        except Exception as e:
            print(f"❌ Не удалось нажать кнопку 'Войти': {e}")
            return False
