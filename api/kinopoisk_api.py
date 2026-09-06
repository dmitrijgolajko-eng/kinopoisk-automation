import requests
from config import KP_API_URL, KP_API_KEY


class KinopoiskAPI:
    def __init__(self):
        self.base_url = KP_API_URL
        self.api_version = "v1.4"
        self.headers = {
            "X-API-KEY": KP_API_KEY,
            "Content-Type": "application/json"
        }

    def _request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}/{self.api_version}/{endpoint}"
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=10
            )
            return response
        except requests.exceptions.Timeout:
            raise Exception(f"Запрос к {url} превысил таймаут в 10 секунд")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка сети при запросе к {url}: {e}")

    def get_movie_by_id(self, movie_id: int):
        url = f"{self.base_url}/v1.4/movie/{movie_id}"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def search_movies(self, query: str, page: int = 1, limit: int = 10, year: int = None, type: str = None):
        """
        Поиск фильмов с поддержкой фильтрации
        :param query: поисковый запрос
        :param page: номер страницы результатов
        :param limit: количество результатов на странице
        :param year: год выпуска (опционально)
        :param type: тип контента (movie/serial/show)
        """
        url = f"{self.base_url}/v1.4/movie/search"
        params = {
            "query": query,
            "page": page,
            "limit": limit
        }

        if year is not None:
            params["year"] = year

        if type is not None:
            params["type"] = type

        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_reviews(self, movie_id: int, page: int = 1, limit: int = 10):
        url = f"{self.base_url}/v1.5/review"
        params = {
            "movieId": movie_id,
            "page": page,
            "limit": limit
        }
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_genres(self):
        url = f"{self.base_url}/v1.4/genres"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def search_movies_with_filters(self, query: str, page: int = 1, limit: int = 10, year: int = None,
                                   type: str = None):
        """
        Поиск фильмов с фильтрацией через эндпоинт /movie (а не /movie/search).
        Эндпоинт /movie/search не поддерживает параметры year и type.
        """
        url = f"{self.base_url}/v1.4/movie"
        params = {
            "query": query,
            "page": page,
            "limit": limit
        }

        if year is not None:
            params["year"] = year

        if type is not None:
            params["type"] = type

        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
