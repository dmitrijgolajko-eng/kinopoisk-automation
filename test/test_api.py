import pytest
from allure import title, story
from api.kinopoisk_api import KinopoiskAPI


@pytest.mark.api
@story("API поиск фильмов")
@title("Проверка поиска фильма по названию")
def test_api_search_movie(api_client):
    with step("Выполняем поиск фильма"):
        response = api_client.search_movie("Twin Peaks")

    with step("Проверяем результаты"):
        assert response.status_code == 200
        assert len(response.json().get("results", [])) > 0


@pytest.mark.api
@story("Работа с рейтингами")
@title("Проверка получения рейтинга фильма")
def test_get_movie_rating(api_client):
    with step("Получаем информацию о фильме"):
        response = api_client.get_movie_info(movie_id=12345)

    with step("Проверяем наличие рейтинга"):
        data = response.json()
        assert "rating" in data
        assert isinstance(data["rating"], float)
