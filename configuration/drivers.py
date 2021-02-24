import logging

# from appium import webdriver as appium_driver

from drivers.playwright_wrapper import Firefox, Chromium, Webkit


log = logging.getLogger(__name__)


class RegisteredDrivers(object):
    # TODO should some of this be just inside all the drivers...?
    # TODO Move this into .yaml if reasonable
    # Maps drivers for later use
    # Impacts how drivers are started and locators are resolved
    BROWSER = "browser"
    CHROMIUM = Chromium
    FIREFOX = Firefox
    WEBKIT = Webkit
    # IOS = Ios
    # ANDROID = Android
    all = (
        FIREFOX,
        CHROMIUM,
        WEBKIT,
        # IOS,
        # ANDROID,
        )

    @classmethod
    def get_driver_by_name(cls, driver_name: str):
        try:
            return {driver.name: driver for driver in cls.all}[driver_name]
        except KeyError:
            log.error(f"Platform driver not found or configured properly: '{driver_name}'")
            # exit properly
