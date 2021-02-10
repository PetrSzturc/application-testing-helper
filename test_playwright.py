from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

from typing import Union
from time import sleep

from pytest import fixture

import logging

from configuration import setup_logging

setup_logging()
log = logging.getLogger(__name__)


class Mapping(object):
    # Maps platform with type of platforms
    # Impacts how locators are resolved
    browser = "browser"
    mobile = "mobile"
    firefox = browser
    chromium = browser
    webkit = browser
    android = mobile
    ios = mobile

class Browsers(object):
    firefox = "firefox"
    chromium = "chromium"
    webkit = "webkit"
    all = (firefox, chromium, webkit)


class Driver(object):

    def __init__(self, headless=False):
        self.platform_driver = None
        self.locator_type = None
        self.headless = headless

    def run_browser(self, browser: Union[Browsers.all]):
        # TODO will see later if the other methods are useless and it's better to use this one directly
        self.platform_driver = CustomPlaywright(browser, self).run()
        # TODO resolve if calling .new_page() here makes sense - I would lose access to new_context() etc.
        self.platform_driver = self.platform_driver.new_page()
        self.locator_type = Mapping.browser
        return self


class CustomPlaywright(object):
    # Wrap around existing Playwright to customise it for running inside this framework
    def __init__(self, 
        browser: str, 
        unified_driver_instance
        ):
        self.unified_driver_instance = unified_driver_instance
        self._browser = sync_playwright().start()
        self.browser = {
            "firefox": self._browser.firefox, 
            "chromium": self._browser.chromium,
            "webkit": self._browser.webkit,
            }.get(browser, "firefox")
        
        # Remap any methods so they are the same across driver for the unified driver
        # self.driver.search_element = self.driver.query_selector
        # self.driver.go_to = self.goto
        
    def _process_args(self):
        # process arguments based on self.unified_driver_instance
        args = {
            "headless": self.unified_driver_instance.headless
        }
        return args

    def run(
        self, 
        # browser,
        ):
        return self.browser.launch(**self._process_args())


# p = sync_playwright().start()
# browser = p.chromium.launch(headless=False)
# page = browser.new_page()

# page.goto("http://seznam.cz")

# sleep(3)
# browser.close()

############################
# with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False)
    # driver = browser.new_page()

driver = Driver()
driver.run_browser(Browsers.chromium)
browser = driver.platform_driver

browser.goto("https://seznam.cz")
search_field = browser.query_selector('div.search-form input[name=q].input')
search_field.fill("chata")
search_field.press('Enter')
sleep(3)
log.info(f"Title: {browser.title()}")
