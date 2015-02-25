# -*- coding: utf-8 -*-
from core.controllers import BaseController
from core.helpers import ForgotPasswordHelper
from core.helpers import ResetPasswordHelper
import teachme_db


class ForgotPasswordController(BaseController):

    def get(self):
        if self.user:
            self.abort(403)
        self.render("forgot_password.html")

    def post(self):
        if self.user:
            self.abort(403)
        email = self.request.get('email')
        sweetAlert = ForgotPasswordHelper.generate_token(email)
        self.render("forgot_password.html", sweetAlert=sweetAlert)


class ResetPasswordController(BaseController):

    def get(self):
        if self.user:
            self.abort(403)
        token_key = self.request.get('tok')
        token = ResetPasswordHelper.valid_token(token_key)
        if token:
            reset_user = token.user.get()
            self.render('reset_password.html', reset_user=reset_user)
        else:
            redirect = '/'
            sweetAlert = ['error', u'El token ya expiró o no existe']
            self.render('reset_password.html', sweetAlert=sweetAlert,
                        redirect=redirect)

    def post(self):
        if self.user:
            self.abort(403)
        token_key = self.request.get('tok')
        token = ResetPasswordHelper.valid_token(token_key)
        if token:
            reset_user = token.user.get()
            password = self.request.get('pw')
            password_con = self.request.get('pw-con')
            if password and password == password_con:
                reset_user.pw_hash = teachme_db.make_pw_hash(reset_user.mail,
                                                             password)
                token.recovered = True
                token.put()
                reset_user.put()
                redirect = "/login"
                sweetAlert = ['success', u'Has cambiado tu contraseña con éxito! :)']
                self.render('reset_password.html', sweetAlert=sweetAlert,
                            redirect=redirect, reset_user=reset_user)
            else:
                sweetAlert = ['error', u'Las contraseñas no concuerdan']
                self.render('reset_password.html', sweetAlert=sweetAlert,
                            reset_user=reset_user)
        else:
            redirect = '/'
            sweetAlert = ['error', u'El token ya expiró o no existe']
            self.render('reset_password.html', sweetAlert=sweetAlert,
                        redirect=redirect)
