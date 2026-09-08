from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class LoginPage(BasePage):
    # Приоритетные селекторы (data-tid от Кинопоиска)
    LOGIN_HEADER_BTN = (
        By.CSS_SELECTOR,
        "button[data-testid='loginHeaderButton']",
    )

    LOGIN_INPUT_FORM = (By.CSS_SELECTOR, "input[data-tid='LoginInput']")
    PASSWORD_INPUT_FORM = (By.CSS_SELECTOR, "input[data-tid='PasswordInput']")
    SUBMIT_BTN_FORM = (By.CSS_SELECTOR, "button[data-tid='SubmitLogin']")

    # Элементы для проверки успеха
    PROFILE_INDICATOR = (
        By.CSS_SELECTOR,
        "a[href*='/my/'] span, span[data-tid='UserAvatar']",
    )

    # Запасные селекторы (fallback), если data-tid пропадет
    FALLBACK_LOGIN_INPUT = (By.CSS_SELECTOR, "input[name='login']")
    FALLBACK_PASS_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    FALLBACK_SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

    def click_login_button(self):
        """Нажимает кнопку 'Войти' в шапке. Сначала закрывает мешающие окна."""
        # ВАЖНО: Всегда закрываем оверлеи перед взаимодействием
        self.close_all_overlays()

        try:
            btn = self.wait.until(
                EC.element_to_be_clickable(self.LOGIN_HEADER_BTN)
            )
            return self._js_click(btn)
        except Exception as e:
            print(f"❌ Ошибка клика по кнопке входа: {e}")
            return False

    def _find_element_with_fallback(
            self, primary_locator, fallback_locator):
        """Вспомогательный метод: ищет по основному селектору,
        если нет - по запасному."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(primary_locator)
            )
        except Exception as e:
            # обработка ошибки
            print(f"Произошла ошибка: {e}")
            # Если основной не найден, пробуем запасной
            try:
                return self.wait.until(
                    EC.visibility_of_element_located(fallback_locator)
                )
            except Exception as e:
                # обработка
                print(f"Произошла ошибка: {e}")

    def login(self, username, password):
        """Заполняет форму авторизации внутри модального окна."""
        # 1. Гарантированно убираем все всплывающие окна
        self.close_all_overlays()

        try:
            # 2. Ищем поля с использованием fallback-логики
            login_field = self._find_element_with_fallback(
                self.LOGIN_INPUT_FORM, self.FALLBACK_LOGIN_INPUT
            )
            pass_field = self._find_element_with_fallback(
                self.PASSWORD_INPUT_FORM, self.FALLBACK_PASS_INPUT
            )
            submit_btn = self._find_element_with_fallback(
                self.SUBMIT_BTN_FORM, self.FALLBACK_SUBMIT_BTN
            )

            if not all([login_field, pass_field, submit_btn]):
                print("❌ Не удалось найти все элементы формы входа.")
                return False

            # 3. Заполняем поля
            login_field.clear()
            login_field.send_keys(username)
            pass_field.clear()
            pass_field.send_keys(password)

            # 4. Нажимаем кнопку
            # Используем JS клик, так как модальные
            # окна часто имеют прозрачные слои поверх кнопки
            if not self._js_click(submit_btn):
                submit_btn.click()
                # Фоллбэк на обычный клик, если JS не сработал

            # 5. Ждем успешного входа
            # Ждем видимости индикатора
            # профиля И изменения URL (защита от ложного срабатывания)
            self.wait.until(
                EC.visibility_of_element_located(self.PROFILE_INDICATOR)
            )

            # Дополнительная проверка: убеждаемся, что мы не на странице логина
            current_url = self.driver.current_url
            if "/login" in current_url or "/auth" in current_url:
                print(
                    "⚠️ Вход выполнен, "
                    "но URL все еще указывает на страницу логина."
                )
                return False

            print("✅ Успешный вход!")
            return True

        except Exception as e:
            print(f"❌ Ошибка при выполнении входа: {e}")
            return False

    def is_login_successful(self, expected_username: str) -> bool:
        """Проверяет, что пользователь вошёл и отображается его имя."""
        try:
            # Используем более надежный XPath с нормализацией пробелов
            locator = (
                By.XPATH,
                f"//span[normalize-space()='{expected_username}']",
            )
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False
