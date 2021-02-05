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


log.info(f"TODO: cleanup driver.driver and similar https://app.clickup.com/t/dn4ea9")


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

    def firefox(self):
        # move this here from init, so that I can call it like
        # Driver().firefox()
        self.locator_type = "browser_locator"
        # self.driver_type = driver_type
        # self.driver = self.driver()
        self.driver = Firefox(executable_path=GeckoDriverManager().install())
        # return self

    def get(self, url):
        return self.driver.get(url)

    def quit(self):
        self.driver.quit()

    def find_element(self, locator):
        pass
        return self.driver.find_element(*getattr(locator, self.locator_type))
        


class AppElement(object):

    def __init__(self,
                 browser_locator = None,
                 android_locator = None,
                 ios_locator = None
                 ):
        self.browser_locator = browser_locator
        self.android_locator = android_locator
        self.ios_locator = ios_locator

    def __get__(self, instance, owner):
        locators_resolution = {
            Chrome: self.browser_locator,
            Firefox: self.browser_locator,
            # Android: self.android_locator,
            # Ios: self.ios_locator,
        }
        return instance.driver.find_element(self)


class BaseSCreen(object):
    def __init__(self, object_with_driver):
        self.driver = object_with_driver.driver


class HomeScreen(BaseSCreen):
    SEARCH_FIELD = AppElement(
        browser_locator=(By.CSS_SELECTOR, 'div.search-form input[name=q].input')
        )

    def search(self, term):
        # log.info(f"HomeScreen.SEARCH_FIELD: {HomeScreen.SEARCH_FIELD}")
        # search_field = self.driver.find_element(HomeScreen.SEARCH_FIELD)
        # search_field.send_keys("chata")
        # search_field.send_keys(Keys.ENTER)
        self.SEARCH_FIELD.send_keys("chata")
        self.SEARCH_FIELD.send_keys(Keys.ENTER)
        sleep(2)


class BaseTest(object):

    def setup_method(self):
        log.info(f"Setup")
        self.driver = Driver()
        self.driver.firefox()
        self.home_screen = HomeScreen(self)

        self.driver.get("https://seznam.cz")

    def teardown_method(self):
        sleep(2)
        log.info("Closing")
        self.driver.quit()


class TestSearch(BaseTest):

    def test_simple_search(self):
        log.info(f"Start test {__name__}")
        self.home_screen.search("chata")
