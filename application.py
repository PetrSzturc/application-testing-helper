import drivers
import app_screens


class AppUi(object):

    def __init__(
        self,
        platform_driver: drivers.BaseCustomDriver,
    ):
        self.platform_driver = platform_driver

        self.home_screen = app_screens.home.HomeScreen(self)
