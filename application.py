from drivers import BaseCustomDriver
import app_screens


class AppUi(object):
    """Represents and contains all screens, their elements and possible actions.

    Any screen you want to use in tests, should be instanced under this object.
    e.g.
      self.home_screen = app_screens.home.HomeScreen(self)
    """

    def __init__(
                 self,
                 platform_driver: BaseCustomDriver,
                ):
        self.platform_driver = platform_driver

        self.home_screen = app_screens.home.HomeScreen(platform_driver)
