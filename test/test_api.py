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

    with step("Проверяем структуру ответа"):
        assert isinstance(response, dict), "Ответ должен быть словарем"

        # Проверяем общие метаданные поиска
        assert "limit" in response, "Отсутствует метаинформация о лимите результатов"
        assert "page" in response, "Отсутствует информация о текущей странице"
        assert "pages" in response, "Отсутствует информация о количестве страниц"
        assert "total" in response, "Отсутствует общее количество результатов"

        # Проверяем основной список результатов
        assert "docs" in response, "В ответе отсутствует поле 'docs'"
        docs = response["docs"]
        assert isinstance(docs, list), "Поле 'docs' должно быть списком"
        assert len(docs) > 0, "Список результатов пуст"

    with step("Проверяем структуру отдельного фильма"):
        first_movie = docs[0]
        assert isinstance(first_movie, dict), "Элемент списка должен быть словарем"

        # Базовые поля фильма
        assert "id" in first_movie, "Отсутствует ID фильма"
        assert "name" in first_movie, "Отсутствует название фильма"
        assert "type" in first_movie, "Отсутствует тип контента"
        assert "year" in first_movie, "Отсутствует год выпуска"

        # Проверяем наличие описания
        assert "description" in first_movie, "Отсутствует описание"
        assert "shortDescription" in first_movie, "Отсутствует краткое описание"

        # Проверяем возрастные ограничения
        assert "ageRating" in first_movie, "Отсутствует возрастное ограничение"

        # Проверяем рейтинги
        assert "rating" in first_movie, "Отсутствует рейтинг"
        rating = first_movie["rating"]
        assert isinstance(rating, dict), "Рейтинг должен быть словарем"

        # Проверяем внешние ID
        assert "externalId" in first_movie, "Отсутствуют внешние ID"
        external_ids = first_movie["externalId"]
        assert isinstance(external_ids, dict), "Внешние ID должны быть словарем"

        # Проверяем постеры
        assert "poster" in first_movie, "Отсутствует информация о постере"
        poster = first_movie["poster"]
        assert isinstance(poster, dict), "Постер должен быть словарем"
        assert "previewUrl" in poster, "Отсутствует превью постера"
        assert "url" in poster, "Отсутствует полный URL постера"


@pytest.mark.api
@story("Работа с рейтингами")
@title("Проверка получения рейтинга фильма по динамическому ID")
def test_get_movie_rating(api_client: KinopoiskAPI):
    search_query = "Twin Peaks"

    with step(f"Находим ID фильма '{search_query}' через поиск"):
        search_response = api_client.search_movies(search_query)

        assert isinstance(search_response, dict), "Ответ должен быть словарем"

        docs = search_response.get("docs", [])
        assert len(docs) > 0, f"Не удалось найти фильм '{search_query}' для проверки рейтинга"

        target_movie = docs[0]
        movie_id = target_movie.get("id")
        assert movie_id is not None, "У найденного фильма отсутствует ID"

        print(f"Используем для теста фильм: '{target_movie.get('name')}' (ID: {movie_id})")

    with step(f"Получаем информацию о фильме с ID {movie_id}"):
        response = api_client.get_movie_by_id(movie_id=movie_id)

    with step("Проверяем наличие валидного рейтинга"):
        assert isinstance(response, dict), "Ответ должен быть словарем"

        # Проверяем основные поля фильма
        assert "id" in response, "Отсутствует ID фильма"
        assert "name" in response, "Отсутствует название фильма"
        assert "type" in response, "Отсутствует тип контента"
        assert "year" in response, "Отсутствует год выпуска"

        # Проверяем рейтинг
        assert "rating" in response, "В ответе отсутствует поле 'rating'"
        rating_data = response["rating"]
        assert isinstance(rating_data, dict), "Рейтинг должен быть словарем"

        # Проверяем наличие хотя бы одного рейтинга
        assert rating_data, "Словарь рейтингов пуст"

        # Проверяем конкретные рейтинги с учетом их шкал
        for rating_source, rating_value in rating_data.items():
            with step(f"Проверяем рейтинг от {rating_source}"):
                assert isinstance(rating_value, (float,
                                                 int)), f"Рейтинг {rating_source} должен быть числом, получен {type(rating_value)}"

                if rating_source == 'russianFilmCritics':
                    # Для критиков может быть шкала до 100
                    assert 0 <= rating_value <= 100, f"Рейтинг {rating_source} вне допустимого диапазона [0, 100]: {rating_value}"
                else:
                    # Для остальных рейтингов шкала 0-10
                    assert 0 <= rating_value <= 10, f"Рейтинг {rating_source} вне допустимого диапазона [0, 10]: {rating_value}"

        # Проверяем голоса
        assert "votes" in response, "Отсутствуют данные о голосах"
        votes_data = response["votes"]
        assert isinstance(votes_data, dict), "Данные о голосах должны быть словарем"

        # Проверяем основные поля фильма
        assert "description" in response, "Отсутствует описание"
        assert "shortDescription" in response, "Отсутствует краткое описание"

        # Проверяем возрастные ограничения
        assert "ageRating" in response, "Отсутствует возрастное ограничение"

        # Проверяем жанры
        assert "genres" in response, "Отсутствуют жанры"
        genres = response["genres"]
        assert isinstance(genres, list), "Жанры должны быть списком"

        # Проверяем страны
        assert "countries" in response, "Отсутствуют страны"
        countries = response["countries"]
        assert isinstance(countries, list), "Страны должны быть списком"

        # Проверяем постеры
        assert "poster" in response, "Отсутствует информация о постере"
        poster = response["poster"]
        assert isinstance(poster, dict), "Постер должен быть словарем"
        assert "previewUrl" in poster, "Отсутствует превью постера"
        assert "url" in poster, "Отсутствует полный URL постера"

        # Проверяем рейтинг критиков
        assert "russianFilmCritics" in response.get("rating", {}), "Отсутствует рейтинг российских критиков"

        # Проверяем количество голосов
        if "votes" in response:
            votes_data = response["votes"]
            for source, count in votes_data.items():
                with step(f"Проверяем количество голосов от {source}"):
                    assert isinstance(count, int), f"Количество голосов {source} должно быть целым числом"
                    assert count >= 0, f"Количество голосов {source} должно быть неотрицательным"

        # Проверяем наличие основной информации
        assert "type" in response, "Отсутствует тип контента"
        assert "year" in response, "Отсутствует год выпуска"
        assert "ageRating" in response, "Отсутствует возрастное ограничение"

        with step("Проверяем информацию о длительности"):
            # Добавляем проверку существования ключа
            # assert "movieLength" in response, "Отсутствует информация о длительности"

            # Дополнительно можно добавить проверку типа данных
            if "movieLength" in response:
                assert isinstance(response["movieLength"], str), "Неверный тип данных для длительности"

            if "isSeries" in response:
                assert isinstance(response["isSeries"], bool), "Флаг сериала должен быть булевым"
                if response["isSeries"]:
                    assert "totalSeriesLength" in response, "Отсутствует общая длительность сериала"
                    assert "seriesLength" in response, "Отсутствует длительность серии"

        # Проверяем информацию о доступности билетов
        assert "ticketsOnSale" in response, "Отсутствует информация о доступности билетов"
        assert isinstance(response["ticketsOnSale"], bool), "Флаг доступности билетов должен быть булевым"

        # Проверяем альтернативные названия
        assert "alternativeName" in response, "Отсутствует альтернативное название"
        # assert "enName" in response, "Отсутствует английское название"

        # Проверяем имена на разных языках
        assert "names" in response, "Отсутствует информация о названиях на разных языках"
        names = response["names"]
        assert isinstance(names, list), "Названия должны быть списком"
        for name_info in names:
            assert "language" in name_info, "Отсутствует информация о языке названия"
            assert "name" in name_info, "Отсутствует само название"
            assert "type" in name_info, "Отсутствует тип названия"
