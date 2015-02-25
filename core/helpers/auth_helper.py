# -*- coding: utf-8 -*-
from core.helpers import BaseHelper
from core.models import RecoverAccountToken
from teachme_db import user as User
from google.appengine.ext import ndb
import datetime
import logging


class ForgotPasswordHelper(BaseHelper):

    @classmethod
    def generate_token(cls, email=None):
        if email:
            user = User.get_by_email(email)
            if user:
                token = RecoverAccountToken.create(user.key)
                nombre = user.name
                link = 'https://www.teachmeapp.com/account/reset?tok=' + token
                subject = 'Reestablecer contraseña'
                mail_body = u"""
                Hola {nombre};

                Parece que has olvidado tu contraseña. En el siguiente link la podrás reestablecerla:
                {link}.

                Este link solo estará activo por las siguientes 24 horas.

                Saludos;

                El equipo de Teachme
                """.format(nombre=nombre, link=link)
                cls.send_email(user, subject, mail_body)
                logging.info('Link for ' + user.name + ' is: ' + link)
                return ['success', u'Te hemos enviado un correo con las instrucciones para que recuperes tu cuenta']
            else:
                logging.info('not user ')
                return ['error', u'Lo sentimos :( no hemos encontrado tu correo en nuestra base de datos']
        else:
            logging.info('not mail ')
            return ['error', u'Debes de ingresar un correo']


class ResetPasswordHelper(BaseHelper):

    @classmethod
    def valid_token(cls, token_key=None):
        if token_key:
            token = ndb.Key(urlsafe=token_key).get()
            if token:
                yesterday = datetime.datetime.now() -\
                    datetime.deltatime(days=1)
                if token.created > yesterday:
                    return token
                else:
                    return False

            else:
                return False
        else:
            return False
