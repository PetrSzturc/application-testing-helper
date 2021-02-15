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
    def __init__(self, locator_type, name, driver_to_run):
        self.locator_type = locator_type
        self.name = name
        self.driver_to_run = driver_to_run


class Hat(object):
# TODO a) this class should only control the others drivers, not have logic as "select element"
#  or b) it has to have all the logic
#  a) -> rename it: director, operator, driver runner
#  b) -> wrap everything into here

    def __init__(self, headless=False):
        self.platform_driver = None
        self.locator_type = None
        self.headless = headless

    def start_platform(self, driver_type: DriverType):
        # TODO This will be modified with appium and other drivers in mind
        driver_to_run = driver_type.driver_to_run
        self.locator_type = driver_type.locator_type
        self.platform_driver = driver_to_run(self).run(driver_type)
        return self

    def select_element(self, app_element):
        # If called from/with AppElement, take correct platform locator from it
        if isinstance(app_element, AppElement):
            locator = getattr(app_element, self.locator_type)
            return self.platform_driver.select_element(locator)
        # If called with just locator:
        return self.platform_driver.select_element(app_element)


class BaseCustomDriver(object):

    def __init__(self,
        hat_instance: Hat,
        ):
        self.hat = hat_instance

    
    def _process_args(self,):
        """
        Takes any arguments and passes them
        """
        return {
            "headless": self.hat.headless
        }

    def _remap_methods(self,):
        log.warn(f"Implement me. {__name__}")


    def open_app(self):
        log.warn(f"Implement me. {__name__}")

    # TODO Consider implementing this here with general way that would work with minimal work on custom driver itself
    # def run(self,):
    #     pass


class CustomPlaywright(BaseCustomDriver):
    # Wrap around existing Playwright to customise it for running inside this framework

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
        #  It doesnt, haha. Move it outside. = expose browser itself + tab itself. Yet todo.
        self.tab_instance = browser_launcher.launch(**self._process_args()).new_page()
        self.tab_instance = self._remap_methods(self.tab_instance)
        return self.tab_instance


class Drivers(object):
    # TODO should thi be just inside all the drivers...?
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

    def __init__(self, hat: Hat):
        self.hat = hat
        self.platform_driver = self.hat.platform_driver

        self.home_screen = HomeScreen(self)


class BaseScreen(object):
    def __init__(self, app: AppUi):
        self.hat = app.hat
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
        return instance.hat.select_element(self)
    
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
def hat():
    log.info(f"Setting up test case.")
    hat = Hat()
    hat.start_platform(Drivers.FIREFOX)
    hat.platform_driver.go_to("https://seznam.cz")
    return hat


@fixture
def app(hat):
    appui = AppUi(hat)
    yield appui
    log.info(f"Cleaning up.")
    appui.platform_driver.close()


def test_simple_search(app):
    app.home_screen.search("chata")
    sleep(2)
    log.info(f"Title: {app.platform_driver.title()}")
