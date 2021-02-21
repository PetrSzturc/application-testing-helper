class BaseScreen(object):
    def __init__(
                 self,
                 app,  #: application.AppUi
                 ):
        self.native_driver = app.native_driver
