from urllib.parse import urlparse

import allure
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import KP_BASE_URL
from pages.main_page import MainPage
from pages.movie_page import MoviePage
from pages.profile_page import ProfilePage
from pages.search_page import SearchPage

# Актуальный ID фильма
TEST_MOVIE_ID = 258687  # Интерстеллар
TEST_MOVIE_URL = f"{KP_BASE_URL}/film/{TEST_MOVIE_ID}/"


@allure.feature("Главная страница")
@allure.story("Проверка элементов и навигации")
@pytest.mark.ui
def test_main_page_elements(driver):
    main_page = MainPage(driver, KP_BASE_URL)

    with allure.step("Открываем главную страницу и убираем оверлеи"):
        main_page.open()
        main_page.close_all_overlays()

    with allure.step("Проверяем домен сайта"):
        parsed_url = urlparse(driver.current_url)
        assert parsed_url.netloc.endswith(
            "kinopoisk.ru"
        ), f"Неверный домен: {parsed_url.netloc}"

    with allure.step(
        "Проверяем наличие основных элементов (Хедер, Поиск, Профиль, Баннер)"
    ):
        assert main_page.is_header_visible(), "Не виден хедер"
        assert main_page.is_search_input_visible(), "Не видно поле поиска"
        assert main_page.is_profile_button_visible(), "Не видна кнопка профиля"
        assert main_page.is_banner_visible(), "Не виден промо-блок"

    with allure.step(
        "Кликаем по баннеру и проверяем переход на страницу фильма"
    ):
        current_url = driver.current_url
        assert main_page.click_banner_movie(), "Не удалось кликнуть по баннеру"
        main_page.wait.until(lambda d: d.current_url != current_url)
        assert (
            "/film/" in driver.current_url
        ), f"Неверный URL после клика: {driver.current_url}"

    print(f"✅ Тест пройден! URL: {driver.current_url}")


@allure.feature("Поиск")
@allure.story("Функционал поиска")
@pytest.mark.ui
def test_search_functionality(driver):
    """Тест 2: Проверка работы поиска."""
    search_page = SearchPage(driver, KP_BASE_URL)

    with allure.step("Открываем страницу поиска и убираем оверлеи"):
        search_page.open()
        search_page.close_all_overlays()

    query = "Интерстеллар"
    with allure.step(f"Выполняем поиск по запросу '{query}'"):
        search_page.search_movie(query)

    with allure.step("Проверяем, что мы на странице выдачи результатов"):
        # 1. Проверяем, что URL соответствует странице поиска
        assert (
            "/new-search/" in driver.current_url
        ), f"Неверная страница: {driver.current_url}"

    with allure.step("Проверяем, что результаты поиска отобразились"):
        # 2. Проверяем наличие карточек фильмов на странице
        count = search_page.get_search_results_count()
        assert (
            count > 0
        ), f"Не найдено ни одной карточки фильма. Найдено: {count}"

        # 3. Проверяем текст первой карточки
        first_result_text = search_page.driver.find_element(
            By.CSS_SELECTOR, 'div[data-test-id="movie-list-item"]'
        ).text
        assert (
            "Интерстеллар" in first_result_text
        ), f"Первый результат не тот: {first_result_text}"


@allure.feature("Страница фильма")
@allure.story("Элементы страницы")
@pytest.mark.ui
def test_movie_page_elements(driver):
    """Тест 3: Проверка постера и заголовка на странице фильма."""
    movie_page = MoviePage(driver, KP_BASE_URL)

    with allure.step(f"Открываем страницу фильма {TEST_MOVIE_ID}"):
        movie_page.open(TEST_MOVIE_URL)
        movie_page.close_all_overlays()

    with allure.step("Проверяем наличие и размер постера"):
        assert (
            movie_page.is_poster_visible()
        ), "Постер не найден или слишком мал"

    with allure.step("Проверяем наличие заголовка фильма"):
        title_locator = (
            By.XPATH,
            "//h1[contains(@class, 'title') "
            "or contains(@class, 'movie-title')]",
        )
        movie_page.wait.until(EC.visibility_of_element_located(title_locator))
        title = driver.find_element(*title_locator)
        assert title.is_displayed(), "Заголовок фильма не виден"

    print("✅ Элементы страницы фильма проверены")


@allure.feature("Страница фильма")
@allure.story("Плеер")
@pytest.mark.ui
def test_video_player_availability(driver):
    movie_page = MoviePage(driver, KP_BASE_URL)

    with allure.step("Открываем страницу фильма и убираем оверлеи"):
        movie_page.open(TEST_MOVIE_URL)
        movie_page.close_all_overlays()

    with allure.step("Наводим курсор на блок трейлера"):
        trailer_container = movie_page.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "aside[class*='trailer']")
            )
        )
        actions = ActionChains(driver)
        actions.move_to_element(trailer_container).perform()
        print("✅ Навели курсор на блок трейлера")

    with allure.step("Ждём появления кнопки «Смотреть трейлер»"):
        wait = WebDriverWait(driver, 45, poll_frequency=0.5)
        try:
            play_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[aria-label*='Смотреть трейлер']")
                )
            )
            print("✅ Кнопка появилась после наведения")
        except TimeoutException:
            driver.save_screenshot("no_play_button.png")
            pytest.fail(
                "Кнопка «Смотреть трейлер» не появилась. Скриншот сохранён."
            )

    with allure.step("Кликаем кнопку «Смотреть трейлер»"):
        # JavaScript-клик обходит перекрывающий слой styles_fade__UKtdM
        driver.execute_script("arguments[0].click();", play_button)
        print("✅ Кнопка нажата (через JavaScript)")

    with allure.step("Ждём появления iframe плеера"):
        wait_player = WebDriverWait(driver, 60, poll_frequency=0.5)
        player_locators = [
            (By.CSS_SELECTOR, "iframe[src*='widgets.kinopoisk.ru']"),
            (By.CSS_SELECTOR, "iframe[src*='player']"),
            (By.CSS_SELECTOR, "iframe[src*='trailer']"),
            (By.CSS_SELECTOR, "iframe[src*='kinopoisk']"),
        ]

        player_found = False
        for locator in player_locators:
            try:
                player = wait_player.until(
                    EC.visibility_of_element_located(locator)
                )
                if player.is_displayed():
                    print(f"✅ Плеер найден по локатору: {locator}")
                    player_found = True
                    break
            except TimeoutException:
                continue

        if not player_found:
            driver.save_screenshot("no_player_after_click.png")
            pytest.fail(
                "Плеер не появился в iframe после клика. Скриншот сохранён."
            )


@allure.feature("Поиск")
@allure.story("Навигация из поиска")
@pytest.mark.ui
def test_search_to_movie_page_navigation(driver):
    """Тест 5: Сквозной переход из поиска на страницу фильма."""
    search_page = SearchPage(driver, KP_BASE_URL)

    with allure.step("Открываем поиск и убираем оверлеи"):
        search_page.open()
        search_page.close_all_overlays()

    query = "Интерстеллар"
    with allure.step(f"Ищем фильм '{query}' и ждем результатов"):
        search_page.search_movie(query)

    # Снова закрываем оверлеи, если появились после поиска
    search_page.close_all_overlays()

    with allure.step(
        "Кликаем по первому результату и проверяем переход на страницу фильма"
    ):
        current_url = driver.current_url

        # Локаторы для клика — от самых точных к общим
        click_locators = [
            (
                By.CSS_SELECTOR,
                'div[data-test-id="movie-list-item"] a[href*="/film/"]',
            ),
            (By.CSS_SELECTOR, 'a[href*="/film/258687"]'),
            (By.CSS_SELECTOR, 'a[href*="/film/"]'),
            (By.CSS_SELECTOR, 'div[data-test-id="movie-list-item"]'),
        ]

        # Отдельный wait с увеличенным таймаутом для перехода
        long_wait = WebDriverWait(driver, 30, poll_frequency=0.5)

        clicked = False
        for locator in click_locators:
            try:
                element = search_page.wait.until(
                    EC.element_to_be_clickable(locator)
                )

                if not element.is_displayed():
                    continue

                # Прокручиваем к элементу
                search_page.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", element
                )

                import time

                time.sleep(0.5)

                # Кликаем
                try:
                    search_page._js_click(element)
                except Exception:
                    element.click()

                print(f"✅ Кликнули по элементу: {locator}")

                # Ждем изменения URL
                try:
                    long_wait.until(lambda d: d.current_url != current_url)
                    clicked = True
                    break
                except TimeoutException:
                    # Возможно, оверлей помешал —
                    # пробуем закрыть и кликнуть снова
                    search_page.close_all_overlays()
                    continue

            except TimeoutException:
                continue

        if not clicked:
            pytest.fail("Не удалось кликнуть ни по одному результату поиска")

    with allure.step("Проверяем переход на страницу фильма с нужным ID"):
        current_url = driver.current_url
        assert (
            str(TEST_MOVIE_ID) in current_url
        ), f"Ожидался фильм с ID {TEST_MOVIE_ID}, но URL: {current_url}"

    print(f"✅ Переход из поиска на страницу фильма {TEST_MOVIE_ID} выполнен")


@allure.feature("Профиль")
@allure.story("Элементы профиля")
@pytest.mark.ui
def test_profile_page_elements(driver):
    """Тест 6: Проверка страницы профиля (с авторизацией через куки)."""
    profile_page = ProfilePage(driver, KP_BASE_URL)

    with allure.step("Открываем профиль (авторизация через куки в фикстуре)"):
        profile_page.open_profile()
        profile_page.close_all_overlays()

    current_url = driver.current_url
    with allure.step("Проверяем, что URL соответствует профилю"):
        # Разрешаем: /my/, /profile/, а также user/<число>
        is_valid = (
            "/my/" in current_url
            or "/profile/" in current_url
            or "/user/" in current_url
            and any(ch.isdigit() for ch in current_url.split("/user/")[-1])
        )
        assert is_valid, f"Неверный URL профиля: {current_url}"

    with allure.step(
        "Проверяем отсутствие кнопки 'Войти' (подтверждение авторизации)"
    ):
        try:
            profile_page.wait.until_not(
                EC.presence_of_element_located(ProfilePage.LOGIN_BTN_LOCATOR)
            )
        except TimeoutException:
            pytest.fail(
                "Кнопка входа всё ещё видна — авторизация не подтверждена"
            )

    print("✅ Элементы страницы профиля проверены")
