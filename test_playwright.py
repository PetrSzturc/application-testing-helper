from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

from appium import webdriver as appium_driver

from time import sleep

from pytest import fixture

import logging

from configuration import setup_logging


class DriverType(object):
    def __init__(self, locator_type, name, driver_to_start):
        self.locator_type = locator_type
        self.name = name
        self.driver_to_start = driver_to_start


class Hat(object):
    """Runner and coordinator that sits on top - hence the name. Plus hat=helper for application testing, haha.\n
    For now takes care of running individual platforms and their drivers.
    """
    # TODO a) this class should only control the others drivers, not have logic as "select element"
    #  or b) it has to have all the logic
    #  a) -> rename it: director, operator, driver runner
    #  b) -> wrap everything into here

    def __init__(self, headless=False):
        self.headless = headless

    def start_platform(self, driver_type: DriverType):
        return driver_type.driver_to_start(self).start(driver_type)


class BaseCustomDriver(object):

    def __init__(self,
        hat_instance: Hat,
        ):
        self.hat = hat_instance  # Used to have access to any arguments passed from above even without passing them explicitly
        self.locator_type = None
        # TODO Consider if this is correct name or: platform_driver or something else
        self.native_driver = None

    def _process_args(self,):
        """
        Takes any arguments and passes them
        """
        return {
            "headless": self.hat.headless,
        }

    def _remap_methods(self,):
        """Remaps any methods so they are the same (name, arguments, return type) across drivers."""
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}.")
        pass

    def _start(self, driver_to_start: DriverType):
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}. Return type should be object to be called; able to .open_app method and control the platform overall. See .start method.")
        pass

    def start(self, driver_to_start: DriverType):
        self.locator_type = driver_to_start.locator_type
        # run method returned by _start and pass arguments to it
        self.native_driver = self._start(driver_to_start)(**self._process_args())
        return self
    
    def open_app(self,):
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}.")
        pass

    def select_element(self, app_element):  # -> AppElement:
        """It is preffered to call this method with AppElement type.\n
        Though for easy use it supports 
        """
        log.debug(f"Looking for element: {app_element}")
        if isinstance(app_element, AppElement):
            return self._select_element(getattr(app_element, self.locator_type))
        # If called with just locator:
        return self._select_element(app_element)

    def _select_element(self, locator):  # -> AppElement:
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}.")
        # implement here calling the native driver method for finding/selecting element
        # e.g. for playwright you would simply put here
        #  return self.tab.query_selector(locator)
        # you may need to process the locator in some way, coming from self.select_element()
        # you should also implement logic to always return (new instance) AppElement even if the element is not present
        #  and set it with proper attributes like .is_present = False/True, .is_displayed = False/True ...
        pass

    def close(self,):
        return self._close()

    def _close(self,):
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}")
        pass
        

class CustomPlaywright(BaseCustomDriver):
    # Wrap around existing Playwright to customise it for running inside this framework

    def _remap_methods(self, obj):

        # Can be called only after new_page is called
        # 
        obj.go_to = obj.goto
        return obj

    def _start(self, driver_to_start: DriverType,):
        # Start playwright
        self.playwright = sync_playwright().start()
        browser_launcher = {
            Drivers.FIREFOX: self.playwright.firefox, 
            Drivers.CHROMIUM: self.playwright.chromium,
            Drivers.WEBKIT: self.playwright.webkit,
        }.get(driver_to_start, self.playwright.firefox)
        return browser_launcher.launch

    def open_app(self, url: str):
        self.tab = self.native_driver.new_page()
        self.tab = self._remap_methods(self.tab)
        self.tab.go_to(f"{url}")
        return self.tab

    def _close(self):
        self.native_driver.close()
        self.playwright.stop()
        
    def _select_element(self, locator):
        # TODO Either here or in BaseCustomDriver implement logic to return AppElement instead of 'NoneType'
        return self.tab.query_selector(locator)

class Drivers(object):
    # TODO should some of this be just inside all the drivers...?
    # TODO Rename to drivers configuration?
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

    def __init__(self, native_driver):
        self.native_driver = native_driver

        self.home_screen = HomeScreen(self)


class BaseScreen(object):
    def __init__(self, app: AppUi):
        self.native_driver = app.native_driver


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
        return instance.native_driver.select_element(self)

    def __str__(self):
        return str({"AppElement": self.__dict__})

    def __repr__(self):
        return self.__str__()
    
    def is_displayed(self):
        # I haven't found a way yet to make this working as I need the instance also here, or some other way to access the driver etc
        if self is None:
            return False
            

class HomeScreen(BaseScreen):
    SEARCH_FIELD = AppElement(browser='div.search-form input')

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


setup_logging()
log = logging.getLogger(__name__)


@fixture
def hat():
    log.info(f"Setting up test case.")
    return Hat()


@fixture
def app(hat: Hat):
    native_driver = hat.start_platform(Drivers.FIREFOX)
    native_driver.open_app(f"https://seznam.cz")
    appui = AppUi(native_driver)
    yield appui
    log.info(f"Cleaning up.")
    native_driver.close()


def test_simple_search(app):
    app.home_screen.search("chata")
    sleep(2)
    log.info(f"Title: {app.native_driver.tab.title()}")
