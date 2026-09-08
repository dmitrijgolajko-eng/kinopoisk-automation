import pytest
import requests
from allure import step, story, title

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
        assert (
            "limit" in response
        ), "Отсутствует метаинформация о лимите результатов"
        assert "page" in response, "Отсутствует информация о текущей странице"
        assert (
            "pages" in response
        ), "Отсутствует информация о количестве страниц"
        assert "total" in response, "Отсутствует общее количество результатов"

        # Проверяем основной список результатов
        assert "docs" in response, "В ответе отсутствует поле 'docs'"
        docs = response["docs"]
        assert isinstance(docs, list), "Поле 'docs' должно быть списком"
        assert len(docs) > 0, "Список результатов пуст"

    with step("Проверяем структуру отдельного фильма"):
        first_movie = docs[0]
        assert isinstance(
            first_movie, dict
        ), "Элемент списка должен быть словарем"

        # Базовые поля фильма
        assert "id" in first_movie, "Отсутствует ID фильма"
        assert "name" in first_movie, "Отсутствует название фильма"
        assert "type" in first_movie, "Отсутствует тип контента"
        assert "year" in first_movie, "Отсутствует год выпуска"

        # Проверяем наличие описания
        assert "description" in first_movie, "Отсутствует описание"
        assert (
            "shortDescription" in first_movie
        ), "Отсутствует краткое описание"

        # Проверяем возрастные ограничения
        assert "ageRating" in first_movie, "Отсутствует возрастное ограничение"

        # Проверяем рейтинги
        assert "rating" in first_movie, "Отсутствует рейтинг"
        rating = first_movie["rating"]
        assert isinstance(rating, dict), "Рейтинг должен быть словарем"

        # Проверяем внешние ID
        assert "externalId" in first_movie, "Отсутствуют внешние ID"
        external_ids = first_movie["externalId"]
        assert isinstance(
            external_ids, dict
        ), "Внешние ID должны быть словарем"

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
        assert (
            len(docs) > 0
        ), f"Не удалось найти фильм '{search_query}' для проверки рейтинга"

        target_movie = docs[0]
        movie_id = target_movie.get("id")
        assert movie_id is not None, "У найденного фильма отсутствует ID"

        print(
            f"Используем для теста фильм:"
            f" '{target_movie.get('name')}' (ID: {movie_id})"
        )

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
                assert isinstance(
                    rating_value, (float, int)
                ), (f"Рейтинг {rating_source} должен быть числом,"
                    f" получен {type(rating_value)}")

                if rating_source == "russianFilmCritics":
                    # Для критиков может быть шкала до 100
                    assert (
                        0 <= rating_value <= 100
                    ), (f"Рейтинг {rating_source} вне допустимого"
                        f" диапазона [0, 100]: {rating_value}")
                else:
                    # Для остальных рейтингов шкала 0-10
                    assert (
                        0 <= rating_value <= 10
                    ), (f"Рейтинг {rating_source} вне допустимого"
                        f" диапазона [0, 10]: {rating_value}")

        # Проверяем голоса
        assert "votes" in response, "Отсутствуют данные о голосах"
        votes_data = response["votes"]
        assert isinstance(
            votes_data, dict
        ), "Данные о голосах должны быть словарем"

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
        assert "russianFilmCritics" in response.get(
            "rating", {}
        ), "Отсутствует рейтинг российских критиков"

        # Проверяем количество голосов
        if "votes" in response:
            votes_data = response["votes"]
            for source, count in votes_data.items():
                with step(f"Проверяем количество голосов от {source}"):
                    assert isinstance(
                        count, int
                    ), f"Количество голосов {source} должно быть целым числом"
                    assert (
                        count >= 0
                    ), (f"Количество голосов {source} должно быть"
                        f" неотрицательным")

        # Проверяем наличие основной информации
        assert "type" in response, "Отсутствует тип контента"
        assert "year" in response, "Отсутствует год выпуска"
        assert "ageRating" in response, "Отсутствует возрастное ограничение"

        with step("Проверяем информацию о длительности"):
            # Добавляем проверку существования ключа
            # assert "movieLength" in response,
            # "Отсутствует информация о длительности"

            # Дополнительно можно добавить проверку типа данных
            if "movieLength" in response:
                assert isinstance(
                    response["movieLength"], str
                ), "Неверный тип данных для длительности"

            if "isSeries" in response:
                assert isinstance(
                    response["isSeries"], bool
                ), "Флаг сериала должен быть булевым"
                if response["isSeries"]:
                    assert (
                        "totalSeriesLength" in response
                    ), "Отсутствует общая длительность сериала"
                    assert (
                        "seriesLength" in response
                    ), "Отсутствует длительность серии"

        # Проверяем информацию о доступности билетов
        assert (
            "ticketsOnSale" in response
        ), "Отсутствует информация о доступности билетов"
        assert isinstance(
            response["ticketsOnSale"], bool
        ), "Флаг доступности билетов должен быть булевым"

        # Проверяем альтернативные названия
        assert (
            "alternativeName" in response
        ), "Отсутствует альтернативное название"
        # assert "enName" in response, "Отсутствует английское название"

        # Проверяем имена на разных языках
        assert (
            "names" in response
        ), "Отсутствует информация о названиях на разных языках"
        names = response["names"]
        assert isinstance(names, list), "Названия должны быть списком"
        for name_info in names:
            assert (
                "language" in name_info
            ), "Отсутствует информация о языке названия"
            assert "name" in name_info, "Отсутствует само название"
            assert "type" in name_info, "Отсутствует тип названия"


@pytest.mark.api
@story("API пагинация результатов")
@title("Проверка корректности пагинации при поиске фильмов")
def test_api_search_pagination(api_client: KinopoiskAPI):
    search_query = "Star Wars"

    with step(f"Запрашиваем первую страницу поиска по '{search_query}'"):
        response_page1 = api_client.search_movies(search_query)

    with step("Проверяем структуру ответа первой страницы"):
        assert isinstance(response_page1, dict)
        assert (
            response_page1.get("page") == 1
        ), "Текущая страница должна быть 1"
        pages = response_page1.get("pages", 1)
        assert pages >= 1, "Должна быть хотя бы одна страница"
        docs1 = response_page1.get("docs", [])
        assert len(docs1) > 0, "Первая страница не должна быть пустой"

    with step(
        "Запрашиваем вторую страницу (если результатов больше одной страницы)"
    ):
        if pages > 1:
            response_page2 = api_client.search_movies(search_query, page=2)

            with step("Проверяем структуру ответа второй страницы"):
                assert isinstance(response_page2, dict)
                assert (
                    response_page2.get("page") == 2
                ), "Текущая страница должна быть 2"
                docs2 = response_page2.get("docs", [])
                assert len(docs2) > 0, "Вторая страница не должна быть пустой"

            with step(
                "Проверяем, что результаты на разных страницах не дублируются"
            ):
                ids_page1 = {movie.get("id") for movie in docs1}
                ids_page2 = {movie.get("id") for movie in docs2}
                overlap = ids_page1 & ids_page2
                assert (
                    len(overlap) == 0
                ), f"Найдены дубликаты ID между страницами: {overlap}"
        else:
            with step(
                "Результатов меньше одной страницы — пагинация не требуется"
            ):
                print(
                    f"Всего страниц: {pages}."
                    f" Пагинация не проверяется (достаточно одной страницы)."
                )


@pytest.mark.api
@story("API обработка несуществующих данных")
@title("Проверка запроса фильма с несуществующим ID")
def test_api_get_nonexistent_movie(api_client: KinopoiskAPI):
    nonexistent_id = 999999999

    with step(f"Запрашиваем фильм с несуществующим ID {nonexistent_id}"):
        try:
            response = api_client.get_movie_by_id(movie_id=nonexistent_id)
            # Если исключения не было — проверяем, что ответ пустой
            if isinstance(response, dict):
                assert (
                    "name" not in response
                ), "API вернул данные фильма для несуществующего ID"
                print("✅ API вернул пустой ответ для несуществующего ID")
        except requests.exceptions.HTTPError as e:
            # 400 — корректный ответ API на несуществующий ID
            status = e.response.status_code
            assert status in (
                400,
                404,
            ), f"Ожидался код 400 или 404, получен {status}"
            print(
                f"✅ API вернул код {status}"
                f" для несуществующего ID — корректная обработка"
            )


@pytest.mark.api
@story("API фильтрация результатов")
@title("Проверка поиска фильма с фильтром по году и типу")
def test_api_search_with_filters(api_client: KinopoiskAPI):
    search_query = "Dune"
    target_year = 2021
    target_type = "movie"

    with step(
        f"Ищем '{search_query}' с фильтром: год={target_year},"
        f" тип={target_type}"
    ):
        # Передаем content_type вместо type
        response = api_client.search_movies_with_filters(
            search_query, year=target_year, content_type=target_type
        )

    with step("Проверяем структуру ответа"):
        assert isinstance(response, dict), "Ответ должен быть словарем"
        assert "docs" in response, "В ответе отсутствует поле 'docs'"
        docs = response["docs"]
        assert isinstance(docs, list), "Поле 'docs' должно быть списком"
        assert (
            len(docs) > 0
        ), "Список результатов пуст после применения фильтров"

    with step("Проверяем, что все результаты соответствуют фильтрам"):
        for i, movie in enumerate(docs):
            with step(f"Проверяем результат #{i + 1}: '{movie.get('name')}'"):
                movie_type = movie.get("type")
                assert (
                    movie_type == target_type
                ), (f"Тип контента не совпадает: "
                    f"ожидаем '{target_type}', получаем '{movie_type}'")

                movie_year = movie.get("year")
                if movie_year is not None:
                    assert (
                        movie_year == target_year
                    ), (f"Год не совпадает: ожидаем {target_year},"
                        f" получаем {movie_year}")
