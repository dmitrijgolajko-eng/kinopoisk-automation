import pytest
from allure import title, story, step
from api.kinopoisk_api import KinopoiskAPI


@pytest.mark.api
@story("API поиск фильмов")
@title("Проверка поиска фильма по названию и релевантность результатов")
def test_api_search_movie(api_client: KinopoiskAPI):
    search_query = "Twin Peaks"

    with step(f"Выполняем поиск фильма по запросу '{search_query}'"):
        response = api_client.search_movies(search_query)

    with step("Проверяем статус код и структуру ответа"):
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        json_data = response.json()
        assert "results" in json_data, "В ответе отсутствует поле 'results'"
        results = json_data["results"]
        assert isinstance(results, list), "Поле 'results' должно быть списком"
        assert len(results) > 0, "Список результатов пуст"

    with step("Проверяем релевантность результатов (наличие искомого фильма)"):
        # Ищем фильм, в названии которого есть "Twin Peaks"
        found_movie = next((movie for movie in results if search_query.lower() in movie.get("title", "").lower()), None)
        assert found_movie is not None, f"Фильм '{search_query}' не найден в результатах поиска"

        # Опционально: можно сохранить ID найденного фильма для следующих тестов
        # Но в рамках одного теста достаточно просто убедиться, что он есть.


@pytest.mark.api
@story("Работа с рейтингами")
@title("Проверка получения рейтинга фильма по динамическому ID")
def test_get_movie_rating(api_client: KinopoiskAPI):
    search_query = "Twin Peaks"

    with step(f"Находим ID фильма '{search_query}' через поиск"):
        search_response = api_client.search_movies(search_query)
        assert search_response.status_code == 200

        results = search_response.json().get("results", [])
        assert len(results) > 0, f"Не удалось найти фильм '{search_query}' для проверки рейтинга"

        # Берем первый фильм из результатов
        target_movie = results
        movie_id = target_movie.get("id")
        assert movie_id is not None, "У найденного фильма отсутствует ID"

        print(f"Используем для теста фильм: '{target_movie.get('title')}' (ID: {movie_id})")

    with step(f"Получаем информацию о фильме с ID {movie_id}"):
        response = api_client.get_movie_by_id(movie_id=movie_id)

    with step("Проверяем статус и наличие валидного рейтинга"):
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        data = response.json()
        assert "rating" in data, "В ответе отсутствует поле 'rating'"

        rating_value = data["rating"]
        # Проверка: рейтинг не None и является числом (float или int)
        assert rating_value is not None, "Рейтинг равен null"
        assert isinstance(rating_value, (float, int)), f"Рейтинг должен быть числом, получен {type(rating_value)}"

        # Дополнительная проверка: рейтинг в разумных пределах (например, от 0 до 10)
        assert 0 <= rating_value <= 10, f"Рейтинг вне допустимого диапазона [0, 10]: {rating_value}"
