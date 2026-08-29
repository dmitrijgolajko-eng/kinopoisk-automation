import requests
from config import API_URL, API_KEY

class KinopoiskAPI:
    def __init__(self):
        self.base_url = API_URL
        self.headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }

    @step("Поиск фильма по ID")
    def get_movie_by_id(self, movie_id: int) -> dict:
        url = f"{self.base_url}/v1.4/movie/{movie_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    @step("Поиск фильмов по запросу")
    def search_movies(self, query: str) -> dict:
        url = f"{self.base_url}/v1.4/movie/search"
        params = {"query": query}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    @step("Получение отзывов о фильме")
    def get_reviews(self, movie_id: int, page: int = 1, limit: int = 10) -> dict:
        url = f"{self.base_url}/v1.5/review"
        params = {
            "movieId": movie_id,
            "page": page,
            "limit": limit
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    @step("Получение информации о жанрах")
    def get_genres(self) -> dict:
        url = f"{self.base_url}/v1.4/genres"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
