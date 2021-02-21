import logging
from pytest import fixture
from time import sleep

# from tests import BaseTest
from configuration import Drivers
from configuration import setup_logging
from hat import Hat
from application import AppUi
from app_element import AppElement

setup_logging()
log = logging.getLogger(__name__)


@fixture
def hat():
    log.info(f"Setting up test case.")
    return Hat()


@fixture
def app(hat: Hat):
    native_driver = hat.start_platform(Drivers.FIREFOX, headless=True)
    native_driver.open_app(f"https://google.com")
    # native_driver.open_app(f"https://seznam.cz")
    appui = AppUi(native_driver)
    yield appui
    log.info(f"Cleaning up.")
    native_driver.close()


def test_simple_search(app):
    app.home_screen.search("chata")
    sleep(2)
    log.info(f"Title: {app.native_driver.tab.title()}")


def test_search_with_app_elements(app):
    app.home_screen.SEARCH_FIELD.type("chata")
    app.home_screen.SEARCH_FIELD.press("Enter")
    sleep(2)
    log.info(f"Title: {app.native_driver.tab.title()}")


def test_directly_using_locators(app):
    search_field = app.native_driver.get_element('input[name="q"]')
    search_field.type("chata")
    search_field.press("Enter")
    log.info(f"Title: {app.native_driver.tab.title()}")


def test_app_element_locators_specified_with_dictionary(app):
    search_field_element = AppElement(locator_dict={"browser": "input[name='q']"})
    log.info(f"Search field element attributes: {search_field_element.__dict__}")
    search_field = app.native_driver.get_element(search_field_element.browser)
    search_field.type("chata")
    search_field.press("Enter")
    log.info(f"Title: {app.native_driver.tab.title()}")
