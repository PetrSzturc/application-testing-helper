import logging
from pytest import fixture
# from time import sleep

from tests.base_test import BaseTest
from configuration import setup_logging
from hat import Hat
from application import AppUi
from app_element import AppElement

setup_logging()
log = logging.getLogger(__name__)


@fixture
def hat():
    log.info(f"Starting Hat.")
    return Hat()


@fixture
def platform_driver(hat: Hat):
    log.info(f"Starting platform and driver.")
    return hat.start_platform_driver('chromium', headless=True)


@fixture
def app(platform_driver):
    platform_driver.open_app(f"https://google.com")
    # platform_driver.open_app(f"https://seznam.cz")
    yield AppUi(platform_driver)
    log.info(f"Cleaning up.")
    platform_driver.close()


def test_simple_search(app: AppUi):
    app.home_screen.search("chata")
    log.info(f"Title: {app.platform_driver.tab.title()}")


def test_search_with_app_elements(app):
    app.home_screen.SEARCH_FIELD.type("chata")
    app.home_screen.SEARCH_FIELD.press("Enter")
    log.info(f"Title: {app.platform_driver.tab.title()}")


def test_directly_using_locators(app, platform_driver):
    search_field = app.platform_driver.get_element('input[name="q"]')
    search_field.type("chata")
    search_field.press("Enter")
    log.info(f"Title: {app.platform_driver.tab.title()}")


def test_app_element_locators_specified_with_dictionary(app):
    search_field_element = AppElement(locator_dict={"browser": "input[name='q']"})
    log.info(f"Search field element attributes: {search_field_element.__dict__}")
    search_field = app.platform_driver.get_element(search_field_element.browser)
    search_field.type("chata")
    search_field.press("Enter")
    log.info(f"Title: {app.platform_driver.tab.title()}")


def test_use_platform_driver_directly(app, platform_driver):
    search_field = platform_driver.get_element('input[name="q"]')
    search_field.type("chata")
    search_field.press("Enter")
    log.info(f"Title: {app.platform_driver.tab.title()}")


class TestClass(BaseTest):
    # Test also the class approach.
    def test_simple_search(self,):
        self.app.home_screen.search("chata")
        log.info(f"Title: {self.app.platform_driver.tab.title()}")
