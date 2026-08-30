import pytest
from allure import title, story, step
from pages.login_page import LoginPage  # Исправлено: нужен отдельный класс для логина
from pages.search_page import SearchPage
from pages.movie_page import MoviePage
from pages.profile_page import ProfilePage
from config import KP_LOGIN, KP_PASSWORD


@pytest.mark.ui
@story("Авторизация пользователя")
@title("Тест авторизации через Яндекс ID")
def test_login_without_phone(driver):
    login_page = LoginPage(driver)
    profile_page = ProfilePage(driver)

    with step("Открытие страницы авторизации"):
        login_page.open()  # Открываем именно страницу логина

    with step("Ввод учетных данных и вход"):
        login_page.login(KP_LOGIN, KP_PASSWORD)

    with step("Ожидание перехода на профиль и проверка авторизации"):
        # Явно ждем, пока мы окажемся на странице профиля
        assert profile_page.is_user_logged_in(), "Пользователь не авторизовался или не перешел на профиль"
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
        count = search_page.get_search_results_count()
        assert count > 0, f"Нет результатов поиска. Найдено: {count}"


@pytest.mark.ui
@story("Работа с контентом")
@title("Проверка добавления в список 'Буду смотреть'")
def test_add_to_watchlist(driver):
    # ВАЖНО: Для этого теста нужно сначала найти фильм и перейти на его страницу.
    # В реальной реализации здесь должна быть логика поиска фильма "Твин Пикс"
    # и перехода на его страницу перед инициализацией MoviePage или передачей URL.
    # Ниже пример с предположением, что open() принимает URL или ID.

    movie_page = MoviePage(driver)

    # Эмуляция перехода на конкретный фильм (замените на реальную логику поиска)
    # Например: movie_page.open(movie_id=12345) или movie_page.open(url="/film/12345")
    # Для примера оставим open(), но помните, что это требует доработки в Page Object.
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
@title("Проверка смены качества видео")
def test_video_quality(driver):
    movie_page = MoviePage(driver)

    # Аналогично предыдущему тесту: нужен переход на конкретный фильм
    movie_page.open()

    with step("Начало воспроизведения"):
        movie_page.start_watching()

    with step("Проверка возможности смены качества"):
        # Сначала убедимся, что кнопка качества вообще видна
        assert movie_page.is_quality_button_visible(), "Кнопка смены качества не найдена"

        current_quality = movie_page.get_video_quality()

        with step(f"Смена качества на HD (текущее: {current_quality})"):
            movie_page.change_video_quality("HD")

        new_quality = movie_page.get_video_quality()
        # Примечание: иногда интерфейс показывает "Авто", даже если выбрано HD.
        # Лучше проверять, что качество изменилось или равно ожидаемому.
        assert new_quality == "HD" or "HD" in new_quality, f"Не удалось сменить качество на HD, текущее: {new_quality}"


@pytest.mark.ui
@story("Работа с оценками")
@title("Проверка выставления оценки")
def test_rate_movie(driver):
    movie_page = MoviePage(driver)

    # Переход на фильм
    movie_page.open()

    with step("Выставление оценки 5 звезд"):
        movie_page.set_rating(5)

    with step("Проверка выставленной оценки"):
        rating = movie_page.get_user_rating()
        assert rating == 5, f"Оценка не сохранилась, текущая: {rating}"

    with step("Сброс оценки"):
        movie_page.reset_rating()
        assert movie_page.get_user_rating() is None, "Оценка не сбросилась"
