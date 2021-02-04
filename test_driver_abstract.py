from appium.webdriver import Remote as appium_driver

from selenium.webdriver import Chrome, Firefox


from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import logging

from configuration.configuration import setup_logging

from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys

setup_logging()
log = logging.getLogger(__name__)


class Driver(object):

    def __init__(
        self, 
        # driver_type
        ):
        mapping = {
            "firefox": (Firefox, "browser"),
            "chrome": (Chrome, "browser"),
            "mobile": (appium_driver, "android"),
        }
        # try:            
            # eg return chrome instance or appium instance
            # self.driver, self.locator_type = mapping[driver_type]
            # self.driver_type = driver_type
            # self.driver = self.driver()
            # return driver()
        # except KeyError:
            # log.error(f"Tried to call driver {driver_type} which isn't configured.")

    def find_element(self, locator):
        self.driver.find_element(*getattr(locator, self.locator_type))
        pass

    def firefox(self):
        # move this here from init, so that I can call it like
        # Driver().firefox()
        self.locator_type = "browser_locator"
        # self.driver_type = driver_type
        # self.driver = self.driver()
        self.driver = Firefox(executable_path=GeckoDriverManager().install())
        return self

    def get(self, url):
        return self.driver.get(url)

    def quit(self):
        self.driver.quit()


class AppElement(object):
    def __init__(
        self,
        android_locator = None,
        browser_locator = None,
        ):
        self.browser_locator = browser_locator


class BaseSCreen(object):
    def __init__(self, driver):
        self.driver = driver


class HomeScreen(BaseSCreen):
    SEARCH_FIELD = AppElement(
        browser_locator=(By.CSS_SELECTOR, 'div.search-form input[name=q].input')
        )

    def search(self, term):
        search_field = self.driver.find_element(HomeScreen.SEARCH_FIELD)
        search_field.send_keys("chata")
        search_field.send_keys(Keys.ENTER)
        sleep(2)


class BaseTest(object):

    def setup_method(self):
        log.info(f"Setup")
        self.app = Driver()
        self.app.firefox()
        self.home_screen = HomeScreen(self.app)

        self.app.get("https://seznam.cz")

    def teardown_method(self):
        log.info("Closing")
        self.app.quit()


class TestSearch(BaseTest):

    def test_simple_search(self):
        log.info(f"Start test {__name__}")
        self.home_screen.search("chata")
