import logging
from abc import ABC, abstractmethod

# from application import AppUi
# from drivers.playwright_wrapper import CustomPlaywright
# TODO Watch for circular imports
# from hat import Hat
from app_element import AppElement


log = logging.getLogger(__name__)


class AbstractDriver(ABC):

    @abstractmethod
    def _start(self, driver_to_start,):
        raise NotImplementedError

    @abstractmethod
    def _open_app(self, *args, **kwargs,):
        raise NotImplementedError

    @abstractmethod
    def _get_element(self, locator,):
        raise NotImplementedError

    # @abstractmethod
    # def _set_driver(self,):
    #     raise NotImplementedError


class BaseCustomDriver(AbstractDriver):
    """Basic implementation with all methods that should every driver support.

    This class should be used to inherit from and implement needed methods.
    You will get warning messages in logs in case a method is missing implementation.
    You should also set all needed attributes per driver implementation.

    Attributes:
    locator_type : str
        Identifies what attribute to select from AppElement by its name.
    name : str
        String by which drivers are resolved to be used for tests. By default set to name of the class.
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
        self.native_driver = None

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

    def _start(self,):
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}. Return type should be callable object;"
                    f"able to .open_app and control the platform overall. See .start method.")
        pass

    def start(self, headless=False):
        log.info(f"Starting platform and driver: {self.locator_type, self.name}")
        # run method returned by _start and pass arguments to it
        self.native_driver = self._start()(headless=headless, **self._process_args())
        return self

    def _open_app(self, **kwargs):
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}.")
        pass

    def open_app(self, url):
        self._open_app(url)

    def get_element(self, app_element):  # -> AppElement:
        """It is preffered to call this method with AppElement type.\n
        Though for easy use it supports calls with just locators as well.
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
        # e.g. for playwright you would simply put here
        #  return self.tab.query_selector(locator)
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
