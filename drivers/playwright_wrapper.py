import logging

from playwright.sync_api import sync_playwright

# from configuration import Drivers
from drivers.drivers import BaseCustomDriver


log = logging.getLogger(__name__)


class CustomPlaywright(BaseCustomDriver):
    """Wrap around existing Playwright to customise it for running inside this framework
    """

    def _remap_methods(self, obj):

        # Can be called only after new_page is called
        obj.go_to = obj.goto
        return obj

    def _open_app(self, url: str):
        # TODO Rewrite this with loading url from configuration
        self.tab = self.native_driver.new_page()
        self.tab = self._remap_methods(self.tab)
        self.tab.go_to(f"{url}")
        return self.tab

    def _close(self):
        self.native_driver.close()
        self.playwright.stop()

    def _get_element(self, locator):
        # TODO Either here or in BaseCustomDriver implement logic to return AppElement instead of 'NoneType'
        return self.tab.query_selector(locator)


class Firefox(CustomPlaywright):
    name = 'firefox'
    locator_type = 'browser'

    def _start(self,):
        # Start playwright
        self.playwright = sync_playwright().start()
        return self.playwright.firefox.launch


class Chromium(CustomPlaywright):
    name = 'chromium'
    locator_type = 'browser'

    def _start(self,):
        # Start playwright
        self.playwright = sync_playwright().start()
        return self.playwright.chromium.launch


class Webkit(CustomPlaywright):
    name = 'webkit'
    locator_type = 'browser'

    def _start(self,):
        # Start playwright
        self.playwright = sync_playwright().start()
        return self.playwright.webkit.launch
