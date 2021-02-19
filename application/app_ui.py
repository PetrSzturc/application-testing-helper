from drivers import BaseCustomDriver
from app_screens import BaseScreen


class AppUi(object):

    def __init__(
        self,
        native_driver#: BaseCustomDriver,
    ):
        self.native_driver = native_driver

        self.home_screen = HomeScreen(self)


class AppElement(object):

    def __init__(self,
                 browser=None,
                 android=None,
                 ios=None,
                 locator_dict: dict = None,
                 ):
        self.browser = browser
        self.android = android
        self.ios = ios
        self.locator_dict = locator_dict
        self._process_locator_dict()

    def __get__(self, instance: BaseScreen, owner):
        # Leave the platform resolution to Driver().
        return instance.native_driver.select_element(self)

    def __str__(self):
        return str({"AppElement": self.__dict__})

    def __repr__(self):
        return self.__str__()

    def _process_locator_dict(self):
        if self.locator_dict:
            for locator_type, locator in self.locator_dict.items():
                setattr(self, locator_type, locator)

    def is_displayed(self):
        # I haven't found a way yet to make this working as I need the instance also here,
        #  or some other way to access the driver etc
        if self is None:
            return False
