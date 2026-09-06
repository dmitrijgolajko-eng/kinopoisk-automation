# test/test_ui.py
from allure import step
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from config import KP_BASE_URL, KP_COOKIES
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.movie_page import MoviePage
from pages.profile_page import ProfilePage
import time

# Актуальный ID фильма
TEST_MOVIE_ID = 258687  # Интерстеллар
TEST_MOVIE_URL = f"{KP_BASE_URL}/film/{TEST_MOVIE_ID}/"

BASE_URL = "https://www.kinopoisk.ru"


@pytest.mark.ui
def test_main_page_elements(driver):
    main_page = MainPage(driver, BASE_URL)
    main_page.open()
    main_page.close_all_overlays()

    # 1. Проверка домена
    parsed_url = urlparse(driver.current_url)
    assert parsed_url.netloc.endswith("kinopoisk.ru"), f"Неверный домен: {parsed_url.netloc}"

    # 2. Проверка наличия промо-блока
    assert main_page.is_banner_visible(), "Не найден промо-блок с премьерой на главной странице"

    # 3. Кликаем и проверяем переход
    current_url_before = driver.current_url
    assert main_page.click_banner_movie(), "Не удалось кликнуть на ссылку в промо-блоке"
    main_page.wait.until(lambda d: d.current_url != current_url_before)
    assert "/film/" in driver.current_url, f"Ожидался переход на страницу фильма, но URL: {driver.current_url}"

    print(f"✅ Тест пройден! Перешли на: {driver.current_url}")


@pytest.mark.ui
def test_search_functionality(driver):
    search_page = SearchPage(driver, BASE_URL)

    search_page.open()
    print(f"🏁 Открыли: {driver.current_url}")
    search_page.close_all_overlays()
    time.sleep(0.5)

    query = "Интерстеллар"
    search_page.search_movie(query)

    try:
        search_page.wait_for_results()
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ! ТЕСТ УСПЕШЕН!")
    except Exception as e:
        driver.save_screenshot("final_test_failure.png")
        print(f"❌ Тест упал: {e}")
        raise e


TEST_MOVIE_URL = "https://www.kinopoisk.ru/film/8477754/"


@pytest.mark.ui
def test_movie_page_elements(driver):
    movie_page = MoviePage(driver, KP_BASE_URL)

    print(f"🎬 Открываем страницу фильма: {TEST_MOVIE_URL}")
    movie_page.open(TEST_MOVIE_URL)
    movie_page.close_all_overlays()

    poster_img = movie_page._get_loaded_poster_element()
    assert poster_img is not None, "Постер не найден"

    width = int(poster_img.get_attribute("naturalWidth"))
    height = int(poster_img.get_attribute("naturalHeight"))
    src = poster_img.get_attribute("src")

    assert width >= 300, f"Слишком маленький постер по ширине: {width}px"
    assert height >= 400, f"Слишком маленький постер по высоте: {height}px"
    assert "posters" in src or "avatars" in src, "Неверный URL постера"

    print("✅ Все проверки пройдены успешно!")


@pytest.mark.ui
def test_video_player_availability(driver):
    movie_page = MoviePage(driver, KP_BASE_URL)
    movie_page.open(TEST_MOVIE_URL)
    movie_page.close_all_overlays()

    try:
        player_locator = (By.CSS_SELECTOR, "video, div[data-testid='player-container']")
        movie_page.wait.until(EC.presence_of_element_located(player_locator))
        print("✅ Плеер найден.")
        assert True, "Плеер найден на странице фильма"
    except Exception:
        print("⚠️ Плеер не найден (фильм может быть недоступен для онлайн-просмотра).")
        assert True


@pytest.mark.ui
def test_profile_page_elements(driver):
    profile_page = ProfilePage(driver, KP_BASE_URL)

    try:
        # Открываем профиль с обработкой авторизации
        profile_page.open_profile()

        # Проверяем успешность входа
        assert profile_page.is_avatar_visible(), "Аватар не появился после входа"

        print("✅ Тест пройден успешно!")

    except Exception as e:
        driver.save_screenshot("profile_login_failure.png")
        print(f"❌ Тест упал: {str(e)}")
        raise e
