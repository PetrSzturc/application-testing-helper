from app_screens import BaseScreen


class HomeScreen(BaseScreen):
    SEARCH_FIELD = AppElement(
        browser='input[name="q"]',
        android='//xpath',
        ios='XCUITestElementField.search',
        )  # Google
    # SEARCH_FIELD = AppElement(browser='div.search-form input')  # Seznam

    def search(self, term: str):
        self.SEARCH_FIELD.fill(term)
        self.SEARCH_FIELD.press("Enter")

    def wait_for_search_results(self):
        # sleep(2)
        pass
