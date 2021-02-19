from application import AppUi


class BaseScreen(object):
    def __init__(self, app: AppUi):
        self.native_driver = app.native_driver
