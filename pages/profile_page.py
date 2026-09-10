from typing import Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class ProfilePage(BasePage):
    # Локатор аватара (как на скриншоте)
    AVATAR_LOCATOR: Tuple[By, str] = (
        By.CSS_SELECTOR,
        'span.styles_icon__GyCFg[style*="background-image"]',
    )
    LOGIN_BTN_LOCATOR: Tuple[By, str] = (
        By.CSS_SELECTOR,
        'button[data-testid="loginHeaderButton"]',
    )

    # Основной URL профиля Кинопоиска
    PROFILE_URL: str = "/my/"

    def open_profile(self) -> None:
        self.open()
        self.close_all_overlays()

        # 1. Сначала проверяем, авторизованы ли мы прямо на Кинопоиске
        if self._is_user_logged_in():
            print("✅ Уже авторизованы на Кинопоиске.")
        else:
            # 2. Если нет — пробуем перейти на профиль,
            # чтобы спровоцировать редирект
            print(
                "🔄 Переходим на страницу профиля для проверки авторизации..."
            )
            profile_url: str = self.base_url.rstrip("/") + self.PROFILE_URL
            self.driver.get(profile_url)
            self.close_all_overlays()

            # 3. Ждем либо появления аватара на Кинопоиске,
            # либо редиректа на Яндекс ID
            try:
                # Ждем аватар на Кинопоиске (если редиректа не было)
                self.wait.until(
                    EC.visibility_of_element_located(self.AVATAR_LOCATOR)
                )
                print("✅ Авторизация подтверждена на Кинопоиске.")
            except TimeoutException:
                # Если таймаут — скорее всего, нас перекинуло на id.yandex.ru
                print(
                    "⚠️ Редирект на Яндекс ID обнаружен."
                    " Проверяем авторизацию там..."
                )

                # Ждем появления имени пользователя или аватара
                # на странице Яндекс ID
                # Ищем по тексту имени (из вашего скриншота)
                # или по специфичному элементу ID
                try:
                    # Вариант А: Ждем появления имени пользователя
                    # (более надежно)
                    name_locator: Tuple[By, str] = (
                        By.XPATH,
                        "//h1[contains(text(), 'Дмитрий')]",
                    )
                    self.wait.until(
                        EC.visibility_of_element_located(name_locator)
                    )
                    print("✅ Авторизация подтверждена на Яндекс ID.")
                except TimeoutException:
                    # Вариант Б: Если имя не нашли,
                    # пробуем найти аватар на странице ID
                    try:
                        self.wait.until(
                            EC.visibility_of_element_located(
                                self.AVATAR_LOCATOR
                            )
                        )
                        print(
                            "✅ Авторизация подтверждена"
                            " по аватару на Яндекс ID."
                        )
                    except TimeoutException:
                        raise Exception(
                            "Не удалось подтвердить авторизацию ни"
                            " на Кинопоиске,"
                            " ни на Яндекс ID. Проверьте куки."
                        )

        # 4. КРИТИЧЕСКИ ВАЖНО: Возвращаемся на Кинопоиск,
        # чтобы тестировать элементы профиля
        print("🔙 Возвращаемся на Кинопоиск для проверки элементов профиля...")
        self.driver.get(self.base_url.rstrip("/") + self.PROFILE_URL)
        self.close_all_overlays()

        # 5. Финальная проверка: ждем,
        # пока страница профиля Кинопоиска загрузится
        # Проверяем, что мы действительно на Кинопоиске и видим элементы
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.AVATAR_LOCATOR)
            )
            print(f"✅ Страница профиля открыта: {self.driver.current_url}")
        except TimeoutException:
            self.driver.save_screenshot("profile_load_error.png")
            raise Exception(
                "Не удалось загрузить страницу профиля "
                "Кинопоиска после возврата. "
                "Сохранил скриншот profile_load_error.png"
            )

    def _is_user_logged_in(self) -> bool:
        try:
            # Проверяем отсутствие кнопки "Войти"
            self.wait.until_not(
                EC.presence_of_element_located(self.LOGIN_BTN_LOCATOR)
            )
            return True
        except TimeoutException:
            # Проверяем наличие аватара
            try:
                self.wait.until(
                    EC.visibility_of_element_located(self.AVATAR_LOCATOR)
                )
                return True
            except TimeoutException:
                return False

    def is_avatar_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.AVATAR_LOCATOR)
            )
            return True
        except TimeoutException:
            return False

