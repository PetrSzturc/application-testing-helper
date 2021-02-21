# from appium import webdriver as appium_driver

from drivers.drivers import DriverType
# from drivers.playwright_wrapper import CustomPlaywright
from drivers.playwright_wrapper import Firefox


class Drivers(object):
    # TODO should some of this be just inside all the drivers...?
    # TODO Rename to drivers configuration?
    # Maps drivers for later use
    # Impacts how drivers are started and locators are resolved
    BROWSER = "browser"
    FIREFOX = DriverType(BROWSER, "firefox", Firefox)
    # CHROMIUM = DriverType(BROWSER, "chromium", CustomPlaywright)
    # WEBKIT = DriverType(BROWSER, "webkit", CustomPlaywright)
    # IOS = DriverType("ios", "ios", appium_driver)
    # ANDROID = DriverType("android", "android", appium_driver)
    all = (
        FIREFOX,
        # CHROMIUM,
        # WEBKIT,
        # IOS,
        # ANDROID,
        )
