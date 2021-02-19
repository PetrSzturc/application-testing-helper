from application import AppUi
from drivers.playwright_wrapper import CustomPlaywright
# TODO Watch for circular imports
from hat import Hat


class DriverType(object):
    """
    .locator_type: Name of the attribute to get the locator from, e.g. browser, ios, android.
    .driver_to_start: Class that can be called to start the platform (driver).
    """
    def __init__(self, locator_type, name, driver_to_start):
        self.locator_type = locator_type
        self.name = name
        self.driver_to_start = driver_to_start


class Drivers(object):
    # TODO should some of this be just inside all the drivers...?
    # TODO Rename to drivers configuration?
    # Maps drivers for later use
    # Impacts how drivers are started and locators are resolved
    BROWSER = "browser"
    FIREFOX = DriverType(BROWSER, "firefox", CustomPlaywright)
    CHROMIUM = DriverType(BROWSER, "chromium", CustomPlaywright)
    WEBKIT = DriverType(BROWSER, "webkit", CustomPlaywright)
    IOS = DriverType("ios", "ios", appium_driver)
    ANDROID = DriverType("android", "android", appium_driver)
    all = (FIREFOX, CHROMIUM, WEBKIT, IOS, ANDROID)


class BaseCustomDriver(object):

    def __init__(self,
                 hat_instance: Hat,
                 ):
        # Used to have access to any arguments passed from above even without passing them explicitly
        self.hat = hat_instance
        self.locator_type = None
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

    def _start(self, driver_to_start: DriverType):
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}. Return type should be callable object;"
                    f"able to .open_app and control the platform overall. See .start method.")
        pass

    def start(self, driver_to_start: DriverType, headless=False):
        self.locator_type = driver_to_start.locator_type
        log.info(f"Starting platform and driver: {driver_to_start.name}")
        # run method returned by _start and pass arguments to it
        self.native_driver = self._start(driver_to_start)(headless=headless, **self._process_args())
        return self

    def _open_app(self,):
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}.")
        pass

    def open_app(self, native_driver):
        self._open_app(native_driver)
        return AppUi(self.native_driver)

    def select_element(self, app_element):  # -> AppElement:
        """It is preffered to call this method with AppElement type.\n
        Though for easy use it supports
        """
        log.debug(f"Looking for element: {app_element}")
        if isinstance(app_element, AppElement):
            return self._select_element(getattr(app_element, self.locator_type))
        # If called with just locator:
        return self._select_element(app_element)

    def _select_element(self, locator):  # -> AppElement:
        # Warn if new driver doesn't have this method implemented.
        log.warning(f"Implement me: {__name__}.")
        # implement here calling the native driver method for finding/selecting element
        # e.g. for playwright you would simply put here
        #  return self.tab.query_selector(locator)
        # you may need to process the locator in some way, coming from self.select_element()
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
