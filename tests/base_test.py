import logging

from application import AppUi
from configuration import Drivers
from hat import Hat


class BaseTest(object):

    def setup_method(self):
        self.log = logging.getLogger(__name__)
        self.log.info(f"Test case setup")
        self.hat = Hat(headless=False)
        self.native_driver = self.hat.start_platform(Drivers.CHROMIUM)
        self.native_driver.open_app(f"https://google.com")
        self.app = AppUi(self.native_driver)

    def teardown_method(self):
        self.log.info(f"Cleaning after test.")
        self.log.info(f"Closing application.")
        self.app.quit()
