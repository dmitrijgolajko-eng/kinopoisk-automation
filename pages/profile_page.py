class ProfilePage(BasePage):
    WATCHLIST = (By.CSS_SELECTOR, ".watchlist")
    FAVORITES = (By.CSS_SELECTOR, ".favorites")

    @step("Проверка списка 'Буду смотреть'")
    def check_watchlist(self):
        return self.wait_for_element(self.WATCHLIST).is_displayed()

    @step("Проверка избранного")
    def check_favorites(self):
        return self.wait_for_element(self.FAVORITES).is_displayed()
