import requests
from config import API_URL, API_KEY


class KinopoiskAPI:
    def __init__(self):
        self.base_url = API_URL
        # Выносим версию API в атрибут, чтобы легко менять в одном месте
        self.api_version = "v1.4"
        self.headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }

    def _request(self, method, endpoint, params=None, data=None):
        """
        Вспомогательный метод для выполнения запросов.
        Добавляет базовый URL, версию, таймаут и возвращает response.
        """
        url = f"{self.base_url}/{self.api_version}/{endpoint}"

        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=10  # Таймаут обязателен для стабильности тестов
            )
            return response
        except requests.exceptions.Timeout:
            raise Exception(f"Запрос к {url} превысил таймаут в 10 секунд")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка сети при запросе к {url}: {e}")

    def get_movie_by_id(self, movie_id: int):
        """Получение информации о фильме по ID"""
        # Для эндпоинтов, где версия отличается (как у отзывов), можно передать полный путь или переопределить логику
        # Но для единообразия лучше использовать базовый метод с явным указанием пути
        url = f"{self.base_url}/v1.4/movie/{movie_id}"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def search_movies(self, query: str):
        """Поиск фильмов по запросу"""
        url = f"{self.base_url}/v1.4/movie/search"
        params = {"query": query}
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_reviews(self, movie_id: int, page: int = 1, limit: int = 10):
        """Получение отзывов о фильме (использует другую версию API)"""
        # Обратите внимание: отзывы на v1.5, поэтому версия не берется из self.api_version
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
        """Получение информации о жанрах"""
        url = f"{self.base_url}/v1.4/genres"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

