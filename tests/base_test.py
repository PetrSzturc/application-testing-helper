import logging

from application import AppUi
from hat import Hat


class BaseTest(object):

    def setup_method(self):
        self.log = logging.getLogger(__name__)
        self.log.info(f"Test case setup")
        self.hat = Hat()
        self.platform_driver = self.hat.start_platform_driver('chromium', headless=False)
        self.platform_driver.open_app(f"https://google.com")
        self.app = AppUi(self.platform_driver)

    def teardown_method(self):
        self.log.info(f"Cleaning after test.")
        self.log.info(f"Closing application.")
        self.platform_driver.close()
