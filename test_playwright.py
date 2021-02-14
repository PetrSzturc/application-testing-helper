from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

from appium import webdriver as appium_driver

from time import sleep

from pytest import fixture

import logging

from configuration import setup_logging

setup_logging()
log = logging.getLogger(__name__)

class DriverType(object):
    def __init__(self, platform_type, name, driver_to_run):
        self.platform_type = platform_type
        self.name = name
        self.driver_to_run = driver_to_run


class Driver(object):

    def __init__(self, headless=False):
        self.platform_driver = None
        self.locator_type = None
        self.headless = headless

    def run_driver(self, driver_type: DriverType):
        # TODO This will be modified with appium and other drivers in mind
        driver_to_run = driver_type.driver_to_run
        self.locator_type = driver_type.platform_type
        self.platform_driver = driver_to_run(self).run(driver_type)
        return self

    def select_element(self, app_element):
        # If called from/with AppElement, take correct platform locator from it
        if isinstance(app_element, AppElement):
            locator = getattr(app_element, self.locator_type)
            return self.platform_driver.select_element(locator)
        # If called with just locator:
        return self.platform_driver.select_element(app_element)

class CustomPlaywright(object):
    # Wrap around existing Playwright to customise it for running inside this framework
    def __init__(self, 
        unified_driver_instance: Driver
        ):
        self.unified_driver_instance = unified_driver_instance

        
    def _process_args(self):
        # process arguments based on self.unified_driver_instance
        args = {
            "headless": self.unified_driver_instance.headless
        }
        return args

    def _remap_methods(self, obj):
        # Can be called only after new_page is called
        # Remap any methods so they are the same across driver for the unified driver
        # TODO think if those are good names
        obj.select_element = obj.query_selector
        obj.go_to = obj.goto
        return obj

    def run(
            self, 
            driver_type: DriverType,
        ):
        self.playwright = sync_playwright().start()
        browser_launcher = {
            Drivers.FIREFOX: self.playwright.firefox, 
            Drivers.CHROMIUM: self.playwright.chromium,
            Drivers.WEBKIT: self.playwright.webkit,
        }.get(driver_type, self.playwright.firefox)
        
        # TODO resolve if calling .new_page() here makes sense - I would lose access to new_context() etc.
        self.tab_instance = browser_launcher.launch(**self._process_args()).new_page()
        self.tab_instance = self._remap_methods(self.tab_instance)
        return self.tab_instance


class Drivers(object):
    # Or drivers configuration?
    # Maps drivers for later use
    # Impacts how drivers are started and locators are resolved
    BROWSER = "browser"
    MOBILE = "mobile"
    FIREFOX = DriverType(BROWSER, "firefox", CustomPlaywright)
    CHROMIUM = DriverType(BROWSER, "chromium", CustomPlaywright)
    WEBKIT = DriverType(BROWSER, "webkit", CustomPlaywright)
    IOS = DriverType(MOBILE, "ios", appium_driver)
    ANDROID = DriverType(MOBILE, "android", appium_driver)
    all = (FIREFOX, CHROMIUM, WEBKIT, IOS, ANDROID)


class AppUi(object):

    def __init__(self, common_driver: Driver):
        self.common_driver = common_driver
        self.platform_driver = self.common_driver.platform_driver

        self.home_screen = HomeScreen(self)


class BaseScreen(object):
    def __init__(self, app: AppUi):
        self.common_driver = app.common_driver
        self.platform_driver = app.platform_driver


class AppElement(object):

    def __init__(self,
                 browser = None,
                 android = None,
                 ios = None
                 ):
        self.browser = browser
        self.android = android
        self.ios = ios

    def __get__(self, instance: BaseScreen, owner):
        # Leave the platform resolution to Driver().
        return instance.common_driver.select_element(self)
    
    def is_displayed(self):
        # I haven't found a way yet to make this working as I need the instance also here, or some other way to access the driver etc
        if self is None:
            return False
            

class HomeScreen(BaseScreen):
    SEARCH_FIELD = AppElement(browser='div.search-form input[name=q].input')

    def search(self, term: str):
        self.SEARCH_FIELD.fill(term)
        self.SEARCH_FIELD.press("Enter")

    def wait_for_search_results(self):
        # sleep(2)
        pass


############################
# with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False)
    # driver = browser.new_page()


@fixture
def common_driver():
    log.info(f"Setting up test case.")
    common_driver = Driver()
    common_driver.run_driver(Drivers.FIREFOX)
    common_driver.platform_driver.go_to("https://seznam.cz")
    return common_driver


@fixture
def app(common_driver):
    appui = AppUi(common_driver)
    yield appui


def test_simple_search(app):
    app.home_screen.search("chata")
    sleep(2)
    # app.common_driver.select_element('div.search-form input[name=q].input')
    log.info(f"Title: {app.platform_driver.title()}")


# common_driver = Driver()
# common_driver.run_driver(Drivers.CHROMIUM)
# driver = common_driver.platform_driver

# driver.goto("https://seznam.cz")
# search_field = driver.select_element('div.search-form input[name=q].input')
# search_field.fill("chata")
# search_field.press('Enter')
# sleep(3)
# log.info(f"Title: {driver.title()}")
