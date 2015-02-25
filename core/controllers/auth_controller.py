from core.controllers import BaseController
from core.helpers import ForgotPasswordHelper


class ForgotPasswordController(BaseController):

    def get(self):
        self.render("forgot_password.html")

    def post(self):
        email = self.request.get('email')
        sweetAlert = ForgotPasswordHelper.generate_token(email)
        self.render("forgot_password.html", sweetAlert=sweetAlert)


class ResetPasswordController(BaseController):

    def get(self):
        token = self.request.get('tok')
        pass

    def post(self):
        pass
