from configuration import RegisteredDrivers
import logging


log = logging.getLogger(__name__)


class Hat(object):
    """Runner and coordinator, controls running individual platforms and their drivers\n
    Sits on top - hence the name. Plus hat=helper for application testing, haha.
    """
    # TODO Add loading configuration and adding it here

    def __init__(self,):
        pass

    def start_platform(self, driver_to_start: str, **kwargs):
        driver = RegisteredDrivers.get_driver_by_name(driver_to_start)
        return driver().start(**kwargs)
