# test_ui.py

import pytest
from allure import title, story, step
from pages.search_page import SearchPage
from pages.movie_page import MoviePage
from pages.profile_page import ProfilePage
from config import KP_LOGIN, KP_PASSWORD


@pytest.mark.ui
@story("Авторизация пользователя")
@title("Тест авторизации через Яндекс ID")
def test_login_without_phone(driver):
    profile_page = ProfilePage(driver)

    with step("Открытие страницы авторизации"):
        profile_page.open()

    with step("Ввод учетных данных"):
        profile_page.login(KP_LOGIN, KP_PASSWORD)

    with step("Проверка успешной авторизации"):
        assert profile_page.is_user_logged_in(), "Пользователь не авторизовался"
        assert profile_page.get_user_login() == KP_LOGIN, "Неверный логин пользователя"


@pytest.mark.ui
@story("Поиск контента")
@title("Проверка поиска фильма")
def test_search_movie(driver):
    search_page = SearchPage(driver)

    with step("Открытие страницы поиска"):
        search_page.open()

    with step("Выполнение поискового запроса"):
        search_page.search("Твин Пикс")

    with step("Проверка результатов поиска"):
        assert search_page.are_search_results_present(), "Результаты поиска не отобразились"
        assert search_page.get_search_results_count() > 0, "Нет результатов поиска"


@pytest.mark.ui
@story("Работа с контентом")
@title("Проверка добавления в список 'Буду смотреть'")
def test_add_to_watchlist(driver):
    movie_page = MoviePage(driver)

    with step("Открытие страницы фильма"):
        movie_page.open()

    with step("Добавление в список 'Буду смотреть'"):
        movie_page.add_to_watchlist()

    with step("Проверка добавления"):
        assert movie_page.is_in_watchlist(), "Фильм не добавился в список"

    with step("Удаление из списка"):
        movie_page.remove_from_watchlist()
        assert not movie_page.is_in_watchlist(), "Фильм не удалился из списка"


@pytest.mark.ui
@story("Воспроизведение видео")
@title("Проверка качества видео")
def test_video_quality(driver):
    movie_page = MoviePage(driver)

    with step("Открытие страницы фильма"):
        movie_page.open()

    with step("Начало воспроизведения"):
        movie_page.start_watching()

    with step("Проверка смены качества"):
        current_quality = movie_page.get_video_quality()
        movie_page.change_video_quality("HD")
        new_quality = movie_page.get_video_quality()
        assert new_quality == "HD", f"Не удалось сменить качество на HD, текущее: {new_quality}"


@pytest.mark.ui
@story("Работа с оценками")
@title("Проверка выставления оценки")
def test_rate_movie(driver):
    movie_page = MoviePage(driver)

    with step("Открытие страницы фильма"):
        movie_page.open()

    with step("Выставление оценки"):
        movie_page.set_rating(5)

    with step("Проверка выставленной оценки"):
        assert movie_page.get_user_rating() == 5, "Оценка не сохранилась"

    with step("Сброс оценки"):
        movie_page.reset_rating()
        assert movie_page.get_user_rating() is None, "Оценка не сбросилась"
