from drivers.drivers import DriverType


class Hat(object):
    """Runner and coordinator, controls running individual platforms and their drivers\n
    Sits on top - hence the name. Plus hat=helper for application testing, haha.
    """
    # TODO Add loading configuration and adding it here

    def __init__(self,):
        pass

    def start_platform(self, driver_type: DriverType, **kwargs):
        return driver_type.driver_to_start(self).start(driver_type, **kwargs)
