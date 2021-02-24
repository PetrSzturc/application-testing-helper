class BaseScreen(object):
    def __init__(
                 self,
                 app,  #: application.AppUi
                 ):
        self.platform_driver = app.platform_driver
