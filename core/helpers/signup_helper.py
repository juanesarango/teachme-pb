# -*- coding: utf-8 -*-
from core.helpers import BaseHelper
from core.models import Company
from teachme_db import user as User
from teachme_db import teacher as Mentor
import re
from webapp2_extras.i18n import gettext as _
import random
import hashlib
from string import letters


class SignupHelper(BaseHelper):

    @classmethod
    def valid_signup(cls, params, pw, pwcon, have_error):
        if not cls.re_valid_name(params['name']):
            params['error_name'] = _(u"El nombre debe contener entre\
             3 y 20 caracteres sin caracteres especiales")
            have_error = True
        if not cls.re_valid_lname(params['lname']):
            params['error_lname'] = _(u"El apellido debe contener entre\
             3 y 20 caracteres sin caracteres especiales")
            have_error = True
        if not cls.re_valid_pw(pw):
            params['error_pw'] = _(u"La contraseña debe contener entre \
                6 y 20 caracteres")
            have_error = True
        elif pw != pwcon:
            params['error_pwcon'] = u"La contraseña debe de coincidir"
            have_error = True
        if not cls.re_valid_mail(params['mail']):
            params['error_mail'] = _(u"El e-mail está erróneo. Ejemplo: \
                email@domain.com")
            have_error = True

        return params, have_error

    @classmethod
    def signup_mail(cls, user, html):
        # To do. Add translation
        subject = user.name + u", Bienvenido a Teachme"
        cls.send_email(user, subject, html)

    @classmethod
    def user_exist(cls, mail):
        user = User.query(User.mail == mail).get()
        if user:
            return user
        else:
            return False

    @classmethod
    def signup_with_facebook(cls, name, lname, mail,
                             fbID, gener, timezoneOffset):
        profile_pic_r = "https://graph.facebook.com/v2.1/"+str(fbID)+"/picture"
        user = User(name=name,
                    lname=lname,
                    mail=name,
                    fbID=int(fbID),
                    gener=gener,
                    timezoneOffset=timezoneOffset,
                    profile_pic_r=profile_pic_r)
        user.put()
        return user

    @classmethod
    def signup_with_company(cls, name, lname, mail,
                            pw, tzo, company):
        pw_hash = cls.make_pw_hash(mail, pw)
        user = User(name=name, lname=lname, mail=mail,
                    pw_hash=pw_hash, timezoneOffset=tzo,
                    company=company)
        user.put()
        mentor = Mentor(name=name, lname=lname, mail=mail,
                        timezoneOffset=tzo, company=company,
                        parent=user.key)
        mentor.put()
        return user, mentor

    @classmethod
    def signup(cls, name, lname, mail, pw, tzo):
        pw_hash = cls.make_pw_hash(mail, pw)
        user = User(name=name, lname=lname, mail=mail,
                    pw_hash=pw_hash, timezoneOffset=tzo)
        user.put()
        return user

    @classmethod
    def is_user_from_company(cls, mail):
        email_domain = mail.split('@')[1]
        company = Company.query(
            Company.email_domain == email_domain).get()
        if company:
            return company
        else:
            return False

    # Regular expresion validation
    @classmethod
    def re_valid_name(cls, name):
        USER_RE = re.compile(r"^.{3,20}$")
        return name and USER_RE.match(name)

    @classmethod
    def re_valid_lname(cls, lname):
        LNAME_RE = re.compile(r"^.{3,20}$")
        return lname and LNAME_RE.match(lname)

    @classmethod
    def re_valid_pw(cls, pw):
        PW_RE = re.compile(r"^.{6,20}")
        return pw and PW_RE.match(pw)

    @classmethod
    def re_valid_mail(cls, mail):
        MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        return not mail or MAIL_RE.match(mail)

    # Password generation
    @classmethod
    def make_salt(cls, length=7):
        return ''.join(random.choice(letters) for x in xrange(length))

    @classmethod
    def make_pw_hash(cls, name, pw, salt=None):
        if not salt:
            salt = cls.make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return '%s,%s' % (salt, h)

    @classmethod
    def valid_pw(cls, name, password, h):
        salt = h.split(',')[0]
        return h == cls.make_pw_hash(name, password, salt)
