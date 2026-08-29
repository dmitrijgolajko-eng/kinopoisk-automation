class MoviePage(BasePage):
    MOVIE_TITLE = (By.CSS_SELECTOR, ".movie-title")
    WATCH_BUTTON = (By.CSS_SELECTOR, ".watch-button")
    FAVORITES_BUTTON = (By.CSS_SELECTOR, ".favorites-button")

    @step("Проверка заголовка фильма")
    def is_movie_title_visible(self):
        return self.wait_for_element(self.MOVIE_TITLE).is_displayed()

    @step("Начало просмотра")
    def start_watching(self):
        self.click(self.WATCH_BUTTON)

    @step("Добавление в избранное")
    def add_to_favorites(self):
        return self.click(self.FAVORITES_BUTTON)
