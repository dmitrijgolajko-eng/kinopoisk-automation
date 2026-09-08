# api/kinopoisk_api.py
import logging

import requests
from requests.exceptions import HTTPError


class KinopoiskAPI:
    def __init__(self, base_url, api_version, headers, timeout=10):
        self.base_url = base_url
        self.api_version = api_version
        self.headers = headers
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def _request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}/{self.api_version}/{endpoint}"
        try:
            self.logger.debug(f"Запрос: {method} {url}")
            self.logger.debug(f"Params: {params}")

            response = requests.request(
                method,
                url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=self.timeout,
            )

            self.logger.debug(f"Статус: {response.status_code}")
            self.logger.debug(f"Ответ: {response.text[:500]}")

            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            self.logger.error(
                f"HTTP ошибка {response.status_code} при запросе к {url}"
            )
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при запросе к {url}: {e}")
            raise

    def search_movies(self, query, page=1, limit=10):
        params = {"query": query, "page": page, "limit": limit}
        return self._request("GET", "movie/search", params=params)

    def get_movie_by_id(self, movie_id):
        return self._request("GET", f"movie/{movie_id}")

    def get_reviews(self, movie_id, page=1, limit=10):
        params = {"movieId": movie_id, "page": page, "limit": limit}
        return self._request("GET", "../v1.5/review", params=params)

    def get_genres(self):
        return self._request("GET", "genres")

    def search_movies_with_filters(
        self, query, page=1, limit=10, year=None, content_type=None
    ):
        params = {"query": query, "page": page, "limit": limit}
        if year is not None:
            params["year"] = year
        if content_type is not None:
            params["type"] = content_type
        return self._request("GET", "movie", params=params)
