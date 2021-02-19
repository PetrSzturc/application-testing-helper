from app_screens import BaseScreen
from application import AppElement


class LoginScreen(BaseScreen):
    username_field = AppElement()
    password_field = AppElement()
    login_button = AppElement()

    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()
