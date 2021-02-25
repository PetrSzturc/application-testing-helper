import logging

from playwright.sync_api import sync_playwright

from drivers.drivers import BaseCustomDriver


log = logging.getLogger(__name__)


class CustomPlaywright(BaseCustomDriver):
    """Wrap around existing Playwright to customise it for running inside this framework.
    """
    locator_type = 'browser'

    def _remap_methods(self, obj):
        # Can be called only after new_page() is called
        obj.go_to = obj.goto
        return obj

    def _open_app(self, url: str):
        # TODO Rewrite this with loading url from configuration
        # TODO Should .tab become app_instance and be universal across platforms?
        self.tab = self.platform_driver.new_page()
        self.tab = self._remap_methods(self.tab)
        self.tab.go_to(f"{url}")
        return self.tab

    def _close(self):
        self.platform_driver.close()
        self.playwright.stop()

    def _get_element(self, locator):
        # TODO Either here or in BaseCustomDriver implement logic to return AppElement instead of 'NoneType'
        return self.tab.query_selector(locator)

    @staticmethod
    def _start_sync_playwright():
        return sync_playwright().start()

    def _start(self, *args, **kwargs):
        self.playwright = sync_playwright().start()
        return self._get_specific_browser().launch(*args, **kwargs)

    def _get_specific_browser(self,):
        # To be implemented in browser specific class
        pass


class Chromium(CustomPlaywright):
    name = 'chromium'

    def _get_specific_browser(self):
        return self.playwright.chromium


class Firefox(CustomPlaywright):
    name = 'firefox'

    def _get_specific_browser(self):
        return self.playwright.firefox


class Webkit(CustomPlaywright):
    name = 'webkit'

    def _get_specific_browser(self):
        return self.playwright.webkit
