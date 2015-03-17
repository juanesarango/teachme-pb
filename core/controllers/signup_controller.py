from core.controllers import BaseController
from core.helpers import SignupHelper
from webapp2_extras.i18n import gettext as _


class SignupController(BaseController):

    def get(self):
        redirect = self.request.get("redirect")
        self.render("signup.html", redirect=redirect)

    def post(self):
        have_error = False
        name = self.request.get('name')
        lname = self.request.get('lname')
        mail = self.request.get('mail')
        pw = self.request.get('pw')
        pwcon = self.request.get('pwcon')
        fbID = self.request.get('fbID')
        gener = self.request.get('gender')
        tzo = int(self.request.get('timezoneOffset'))
        redirect = self.request.get('redirect')

        params = dict(name=name,
                      lname=lname,
                      mail=mail,
                      redirect=redirect)
        if not fbID:
            params, have_error = SignupHelper.valid_signup(params, pw,
                                                           pwcon, have_error)
        if have_error:
            self.render("signup.html", **params)
            return
        else:
            user = SignupHelper.user_exist(mail)
            if user:
                sweetAlert = ['warning', _(u'El email que ingresaste ya se encuentra registrado')]
                self.render('signup.html', sweetAlert=sweetAlert)
            else:
                # if Facebook
                if fbID:
                    user = SignupHelper.signup_with_facebook(name,
                                                             lname,
                                                             mail,
                                                             fbID,
                                                             gener,
                                                             tzo)
                    mentor = None
                else:
                    company = SignupHelper.is_user_from_company(mail)
                    if company:
                        user, mentor = SignupHelper.signup_with_company(
                            name, lname, mail, pw, tzo, company)
                        redirect = '/profile/teacher/{}'.format(mentor.key.id())
                    else:
                        user = SignupHelper.signup(name, lname, mail, pw, tzo)
                        mentor = None
                    enlace = "https://www.teachmeapp.com/user/verify/?r=" + user.key.urlsafe()
                    html = self.render_str("mail_template.html",
                                           sujeto=user.name,
                                           enlace=enlace)
                    SignupHelper.signup_mail(user, html)
                    self.login(user, mentor)
                    sweetAlert = ['success',
                                  _(u'Tu registro ha sido exitoso, Bienvenido :)')]
                    if not redirect:
                        redirect = '/'
                    self.render('signup.html',
                                sweetAlert=sweetAlert,
                                redirect=redirect)
