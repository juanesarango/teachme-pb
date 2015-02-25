from core.controllers import BaseController
from core.helpers import ForgotPasswordHelper
from core.helpers import ResetPasswordHelper


class ForgotPasswordController(BaseController):

    def get(self):
        self.render("forgot_password.html")

    def post(self):
        email = self.request.get('email')
        sweetAlert = ForgotPasswordHelper.generate_token(email)
        self.render("forgot_password.html", sweetAlert=sweetAlert)


class ResetPasswordController(BaseController):

    def get(self):
        token_key = self.request.get('tok')
        token = ResetPasswordHelper.valid_token(token_key)
        if token:
            user = token.user.get()
            self.render('reset_password.html', user=user)
        else:
            sweetAlert = ['error', 'El token ya expiro o no existe']
            self.render('reset_password.html', sweetAlert)

    def post(self):
        pass
