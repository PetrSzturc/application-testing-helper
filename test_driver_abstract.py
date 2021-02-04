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

    def __new__(
        cls, 
        # driver_type
        ):
        mapping = {
            "firefox": Firefox,
            "chrome": Chrome,
            "mobile": appium_driver,
        }
        # try:            
            # eg return chrome instance or appium instance
            # driver = mapping[driver_type]
            # self.driver_type = driver_type
            # return driver()
        # except KeyError:
            # log.error(f"Tried to call driver {driver_type} which isn't configured.")

    def find_element(self, locator):

        pass

    @staticmethod
    def firefox():
        return Firefox(executable_path=GeckoDriverManager().install())


class AppElement(object):
    pass


class BaseSCreen(object):
    def __init__(self, driver):
        self.driver = driver


class HomeScreen(BaseSCreen):
    SEARCH_FIELD = (By.CSS_SELECTOR, 'div.search-form input[name=q].input')

    def search(self, term):
        search_field = self.driver.find_element(*HomeScreen.SEARCH_FIELD)
        search_field.send_keys("chata")
        search_field.send_keys(Keys.ENTER)
        sleep(2)


class BaseTest(object):

    def setup_method(self):
        log.info(f"Setup")
        self.driver = Driver.firefox()
        self.home_screen = HomeScreen(self.driver)

        self.driver.get("https://seznam.cz")

    def teardown_method(self):
        log.info("Closing")
        self.driver.close()
        self.driver.quit()


class TestSearch(BaseTest):

    def test_simple_search(self):
        log.info(f"Start test {__name__}")
        self.home_screen.search("chata")
