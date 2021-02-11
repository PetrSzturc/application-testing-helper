from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

from appium import webdriver as appium_driver

from time import sleep

from pytest import fixture

import logging

from configuration import setup_logging

setup_logging()
log = logging.getLogger(__name__)

class DriverType(object):
    def __init__(self, platform_type, name, driver_to_run):
        self.platform_type = platform_type
        self.name = name
        self.driver_to_run = driver_to_run


class Driver(object):

    def __init__(self, headless=False):
        self.platform_driver = None
        self.locator_type = None
        self.headless = headless

    def run_driver(self, driver_type: DriverType):
        # TODO This will be modified with appium and other drivers in mind
        driver_to_run = driver_type.driver_to_run
        self.platform_driver = driver_to_run(self).run(driver_type)
        return self


class CustomPlaywright(object):
    # Wrap around existing Playwright to customise it for running inside this framework
    def __init__(self, 
        unified_driver_instance: Driver
        ):
        self.unified_driver_instance = unified_driver_instance
        
    def _process_args(self):
        # process arguments based on self.unified_driver_instance
        args = {
            "headless": self.unified_driver_instance.headless
        }
        return args

    def _remap_methods(self, obj):
        # Can be called only after new_page is called
        # Remap any methods so they are the same across driver for the unified driver
        # TODO think if those are good names
        obj.select_element = obj.query_selector
        obj.go_to = obj.goto
        return obj

    def run(
            self, 
            driver_type: DriverType,
        ):
        self.unified_driver_instance.locator_type = driver_type.platform_type
        self.playwright = sync_playwright().start()
        browser_launcher = {
            Drivers.FIREFOX: self.playwright.firefox, 
            Drivers.CHROMIUM: self.playwright.chromium,
            Drivers.WEBKIT: self.playwright.webkit,
        }.get(driver_type, self.playwright.firefox)
        
        # TODO resolve if calling .new_page() here makes sense - I would lose access to new_context() etc.
        new_tab = browser_launcher.launch(**self._process_args()).new_page()
        new_tab = self._remap_methods(new_tab)
        return new_tab


class Drivers(object):
    # Or drivers configuration?
    # Maps drivers for later use
    # Impacts how drivers are started and locators are resolved
    BROWSER = "browser"
    MOBILE = "mobile"
    FIREFOX = DriverType(BROWSER, "firefox", CustomPlaywright)
    CHROMIUM = DriverType(BROWSER, "chromium", CustomPlaywright)
    WEBKIT = DriverType(BROWSER, "webkit", CustomPlaywright)
    IOS = DriverType(MOBILE, "ios", appium_driver)
    ANDROID = DriverType(MOBILE, "android", appium_driver)
    all = (FIREFOX, CHROMIUM, WEBKIT, IOS, ANDROID)


class Driver(object):

    def __init__(self, headless=False):
        self.platform_driver = None
        self.locator_type = None
        self.headless = headless

    def run_driver(self, driver_type: DriverType):
        # TODO This will be modified with appium and other drivers in mind
        try:
            driver_to_run = driver_type.driver_to_run
        except KeyError:
            log.error(f"Driver {driver_type.name} was not properly configured or mapped.")
        self.platform_driver = driver_to_run(self).run(driver_type)
        return self


class CustomPlaywright(object):
    # Wrap around existing Playwright to customise it for running inside this framework
    def __init__(self, 
        unified_driver_instance
        ):
        self.unified_driver_instance = unified_driver_instance
        
    def _process_args(self):
        # process arguments based on self.unified_driver_instance
        args = {
            "headless": self.unified_driver_instance.headless
        }
        return args

    def _remap_methods(self, obj):
        # Can be called only after new_page is called
        # Remap any methods so they are the same across driver for the unified driver
        # TODO think if those are good names
        obj.select_element = obj.query_selector
        obj.go_to = obj.goto
        return obj

    def run(
            self, 
            driver_type: DriverType,
        ):
        self.unified_driver_instance.locator_type = driver_type.platform_type
        self.playwright = sync_playwright().start()
        browser_launcher = {
            Drivers.FIREFOX: self.playwright.firefox, 
            Drivers.CHROMIUM: self.playwright.chromium,
            Drivers.WEBKIT: self.playwright.webkit,
        }.get(driver_type, self.playwright.firefox)
        
        # TODO resolve if calling .new_page() here makes sense - I would lose access to new_context() etc.
        new_tab = browser_launcher.launch(**self._process_args()).new_page()
        new_tab = self._remap_methods(new_tab)
        return new_tab


############################
# with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False)
    # driver = browser.new_page()

common_driver = Driver()
common_driver.run_driver(Drivers.CHROMIUM)
driver = common_driver.platform_driver

driver.goto("https://seznam.cz")
search_field = driver.select_element('div.search-form input[name=q].input')
search_field.fill("chata")
search_field.press('Enter')
sleep(3)
log.info(f"Title: {driver.title()}")
