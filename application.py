import drivers
import app_screens


class AppUi(object):

    def __init__(
        self,
        native_driver: drivers.BaseCustomDriver,
    ):
        self.native_driver = native_driver

        self.home_screen = app_screens.home.HomeScreen(self)
