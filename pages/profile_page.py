# pages/profile_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
from config import KP_BASE_URL, KP_COOKIES
import time


class ProfilePage(BasePage):
    # ТОЧНЫЙ ЛОКАТОР на основе твоего скриншота
    # Ищем img с data-testid="avatar". Этого достаточно.
    AVATAR_LOCATOR = (By.CSS_SELECTOR, 'img[data-testid="avatar"]')

    # Кнопка "Войти" (чтобы проверять отсутствие)
    LOGIN_BTN_LOCATOR = (By.CSS_SELECTOR, 'button[data-testid="loginHeaderButton"]')

    def open_profile(self):
        """Открывает профиль. Авторизация через куки."""
        self.open()
        self.close_all_overlays()

        # 1. Быстрая проверка: может уже авторизованы?
        if self._is_user_logged_in():
            print("✅ Уже авторизованы.")
            return

        # 2. Авторизация через куки
        if KP_COOKIES:
            self._login_with_cookies()
            # Даем время на рендер шапки
            time.sleep(3)

            # Обновляем страницу, чтобы сайт применил сессию
            self.driver.refresh()
            time.sleep(3)

            if self._is_user_logged_in():
                print("✅ Авторизация через куки успешна!")
                return
            else:
                self.driver.save_screenshot("avatar_not_found.png")
                raise Exception(
                    "Куки добавлены, но авторизация не подтверждена. "
                    "Посмотри скриншот avatar_not_found.png. "
                    "Скорее всего, значения в config.py протухли (сессия истекла)."
                )
        else:
            raise ValueError("KP_COOKIES не заданы в config.py!")

    def _is_user_logged_in(self):
        """
        Проверяет авторизацию.
        Приоритет 1: Кнопки 'Войти' нет -> Авторизован.
        Приоритет 2: Аватар есть в DOM -> Авторизован.
        """
        try:
            # Стратегия А: Проверяем, что кнопки "Войти" НЕТ (самый надежный способ)
            from selenium.webdriver.support.ui import WebDriverWait
            short_wait = WebDriverWait(self.driver, 3)

            try:
                # Если кнопка находится за 3 секунды -> НЕ авторизованы
                short_wait.until(EC.presence_of_element_located(self.LOGIN_BTN_LOCATOR))
                return False
            except TimeoutException:
                # Если кнопка НЕ найдена за 3 секунды -> Авторизованы!
                print("✅ Кнопка 'Войти' не найдена. Пользователь авторизован.")
                return True

        except Exception:
            pass

        # Стратегия Б (запасная): Ищем аватар по ТОЧНОМУ локатору из твоего скриншота
        try:
            # Используем presence, так как у аватара aria-hidden="true"
            avatar = self.wait.until(EC.presence_of_element_located(self.AVATAR_LOCATOR))
            return True
        except TimeoutException:
            return False

    def _login_with_cookies(self):
        """Добавляет куки, игнорируя ошибки домена для проблемных кук."""
        print("🍪 Начинаем добавление кук...")

        # 1. Сначала обрабатываем куки для .yandex.ru
        # Заходим на passport.yandex.ru, чтобы контекст домена был верным
        self.driver.get("https://passport.yandex.ru")
        time.sleep(2)

        for cookie in KP_COOKIES:
            domain = cookie.get("domain", "")
            if ".yandex.ru" in domain:
                clean = self._clean_cookie(cookie)
                try:
                    self.driver.add_cookie(clean)
                    print(f"  ✅ Добавлена кука: {cookie['name']} (yandex)")
                except Exception as e:
                    # Игнорируем ошибки домена для yabs-sid и подобных
                    print(f"  ⚠️ Пропущена кука {cookie['name']}: {e}")

        # 2. Теперь обрабатываем куки для .kinopoisk.ru
        self.driver.get(KP_BASE_URL)
        time.sleep(2)

        for cookie in KP_COOKIES:
            domain = cookie.get("domain", "")
            if ".kinopoisk.ru" in domain:
                clean = self._clean_cookie(cookie)
                try:
                    self.driver.add_cookie(clean)
                    print(f"  ✅ Добавлена кука: {cookie['name']} (kinopoisk)")
                except Exception as e:
                    print(f"  ⚠️ Ошибка добавления куки {cookie['name']}: {e}")

    @staticmethod
    def _clean_cookie(cookie_dict):
        """Удаляет поля, которые ломают add_cookie в Selenium."""
        forbidden_keys = ["expiry", "expires", "httpOnly", "secure", "sameSite"]
        return {k: v for k, v in cookie_dict.items() if k not in forbidden_keys}

    def is_avatar_visible(self):
        """Метод для assert в тесте."""
        return self._is_user_logged_in()
