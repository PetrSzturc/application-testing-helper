from appium.webdriver import Remote as appium_driver
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import logging
from time import sleep

from pytest import fixture

from configuration.configuration import setup_logging


setup_logging()
log = logging.getLogger(__name__)


class Driver(object):

    def __init__(
        self, 
        # driver_type,
        ):
        # TODO Specifying drive_type via argument instead of calling firefox() might be better when called from terminal
        mapping = {
            "firefox": (Firefox, "browser"),
            "chrome": (Chrome, "browser"),
            "mobile": (appium_driver, "android"),
        }
        self.platform_driver = None
        self.locator_type = None

    def firefox(self):
        self.locator_type = "browser"
        # TODO setup of platforms should be moved elsewhere
        self.platform_driver = Firefox(executable_path=GeckoDriverManager().install())
        return self

    def go_to(self, url):
        self.platform_driver.get(url)

    def quit(self):
        self.platform_driver.quit()

    def find_element(self, app_element) -> WebElement:
        # Select appropriate locator and pass it based on running driver->locator type
        if isinstance(app_element, AppElement):
            return self.platform_driver.find_element(*getattr(app_element, self.locator_type))
        return self.platform_driver.find_element(*app_element)
        

class AppUi(object):

    def __init__(self, driver: Driver):
        self.driver = driver
        self.home_screen = HomeScreen(self)


class BaseScreen(object):
    def __init__(self, app: AppUi):
        self.driver = app.driver
        

class AppElement(object):

    def __init__(self,
                 browser = None,
                 android = None,
                 ios = None
                 ):
        self.browser = browser
        self.android = android
        self.ios = ios

    def __get__(self, instance: BaseScreen, owner) -> WebElement:
        # Leave the platform resolution to Driver().
        return instance.driver.find_element(self)


class HomeScreen(BaseScreen):
    SEARCH_FIELD = AppElement(
        browser=(By.CSS_SELECTOR, 'div.search-form input[name=q].input'),
        )

    def search(self, term):
        assert self.SEARCH_FIELD.is_displayed()
        self.SEARCH_FIELD.send_keys("chata")
        self.SEARCH_FIELD.send_keys(Keys.ENTER)
        log.info(f"Searching for: {term}.")


# Simplify usage for both test functions and test classes.
def _setup() -> AppUi:
    log.info(f"Test setup.")
    driver = Driver().firefox()
    app = AppUi(driver)
    driver.go_to("https://seznam.cz")
    return app

def _teardown(app: AppUi):
    # TODO sleep
    sleep(2)

    log.info(f"Test teardown.")
    app.driver.quit()


class BaseTest(object):

    def setup_method(self):
        self.app = _setup()

    def teardown_method(self):
        _teardown(self.app)


class TestSearch(BaseTest):

    def test_simple_search(self):
        self.app.home_screen.search("chata")


@fixture
def app():
    app = _setup()
    yield app
    _teardown(app)


def test_simple_search(app: AppUi):
    app.home_screen.search("chata")


def test_with_adhoc_elements(app: AppUi):
    search_field = app.driver.find_element((By.CSS_SELECTOR, 'div.search-form input[name=q].input'))
    assert search_field.is_displayed()
    search_field.send_keys("chata")
    search_field.send_keys(Keys.ENTER)

    
def test_with_predefined_elements(app: AppUi):
    assert app.home_screen.SEARCH_FIELD.is_displayed()
    app.home_screen.SEARCH_FIELD.send_keys("chata")
    app.home_screen.SEARCH_FIELD.send_keys(Keys.ENTER)
