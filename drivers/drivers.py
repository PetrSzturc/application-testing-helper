import logging
from abc import ABC, abstractmethod

# from application import AppUi
# from drivers.playwright_wrapper import CustomPlaywright
# TODO Watch for circular imports
# from hat import Hat
from app_element import AppElement


log = logging.getLogger(__name__)


class AbstractDriver(ABC):
    # TODO research and decide if to use AbstractClass
    #   The main criteria is intuitivness especially for people from outside.
    #   So that anyone writing their own driver easily understands what needs to be done, based on:
    #       a log.error message with "Implement me __name__" or abstract class?
    #   With abstract the BaseCustomDriver would be a bit cleaner.
    #   It can also be implemented as another super class to inherit from;
    #       with just the empty methods, not being abstract

    @abstractmethod
    def _start(self, driver_to_start,):
        raise NotImplementedError

    @abstractmethod
    def _open_app(self, *args, **kwargs,):
        raise NotImplementedError

    @abstractmethod
    def _get_element(self, locator,):
        raise NotImplementedError

    @abstractmethod
    def _close(self,):
        raise NotImplementedError


class BaseCustomDriver(AbstractDriver):
    """Basic implementation with all methods that should every driver support.

    When implementing custom driver, you should inherit from this class and implement needed methods.
    You should implement (overwrite) methods only with underscore, e.g. _start()
        as start() etc. is exposed to test and its behaviour shouldn't alter between platforms.
    You will get warning messages in logs in case a method is missing its implementation.
    You should also set all needed attributes per driver implementation.

    Attributes:

    locator_type : str
        Identifies what attribute to select from AppElement by its name. e.g. 'browser', 'android', 'ios'

    name : str
        String by which drivers are resolved to be used for tests.
    """

    # TODO implement these also into abstract class if possible
    name: str
    locator_type: str

    def __init__(self,
                 ):
        # Used to have access to any arguments passed from above even without passing them explicitly
        self.locator_type = self.locator_type
        self.name = self.name
        # TODO Consider if this is correct name or: platform_driver or something else
        self.platform_driver = None

    def _process_args(self,):
        """
        Takes arguments, attributes, parameters from Hat and passes them to drivers.
        """
        return {}

    def _remap_methods(self,):
        """Remaps any methods so they are the same (name, arguments, return type) across drivers."""
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}.")
        pass

    def _start(self, *args, **kwargs):
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}.")
        pass

    def start(self, headless=False):
        log.info(f"Starting platform and driver: {self.locator_type, self.name}")
        # run method returned by _start() and pass arguments to it
        self.platform_driver = self._start(headless=headless, **self._process_args())
        return self

    def _open_app(self, **kwargs):
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}.")
        pass

    def open_app(self, url):
        # TODO open_app
        self._open_app(url)

    def get_element(self, app_element):  # -> AppElement:
        """It is preffered to call this method with AppElement type.\n
        Though for easy use it supports calls with bare locators as well.
        """
        log.debug(f"Looking for element: {app_element}")
        if isinstance(app_element, AppElement):
            return self._get_element(getattr(app_element, self.locator_type))
        # If called with just locator:
        return self._get_element(app_element)

    def _get_element(self, locator):  # -> AppElement:
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}.")
        # implement here calling the native driver method for finding/selecting element
        # e.g. for playwright you would write something like:
        #   return self.tab.query_selector(locator)
        # you may need to process the locator in some way, coming from self.get_element()
        # you should also implement logic to always return (new instance) AppElement even if the element is not present
        #  and set it with proper attributes like .is_present = False/True, .is_displayed = False/True ...
        pass

    def close(self,):
        log.info(f"Closing platform and driver.")
        return self._close()

    def _close(self,):
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}")
        pass
