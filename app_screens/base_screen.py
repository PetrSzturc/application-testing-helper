class BaseScreen(object):
    def __init__(
                 self,
                 platform_driver
                 ):
        # Platform driver is needed here, so that later .get_element methods can call it.
        self.platform_driver = platform_driver
