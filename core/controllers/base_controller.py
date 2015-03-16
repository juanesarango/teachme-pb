import webapp2
import jinja2
import json
import datetime

import fns
import jinja_fns
import teachme_db

from google.appengine.ext import ndb
from webapp2_extras import i18n
from webapp2_extras.i18n import gettext as _
from core.helpers import TwitchHelper


class BaseController(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        # first, try and set locale from cookie
        locale = request.cookies.get('locale')
        if locale in jinja_fns.AVAILABLE_LOCALES:
            i18n.get_i18n().set_locale(locale)
        else:
            # if that failed, try and set locale from accept language header
            header = request.headers.get('Accept-Language', '')  # e.g. en-gb,en;q=0.8,es-es;q=0.5,eu;q=0.3
            locales = [locale.split(';')[0] for locale in header.split(',')]
            for locale in locales:
                if locale in jinja_fns.AVAILABLE_LOCALES:
                    i18n.get_i18n().set_locale(locale)
                    break
            else:
                # if still no locale set, use the first available one
                i18n.get_i18n().set_locale(jinja_fns.AVAILABLE_LOCALES[0])

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        suggestions = []
        self.areas = teachme_db.areas.query().order(teachme_db.areas.name)
        for l in self.areas:
            suggestions.append(l.name)
        teachers = teachme_db.teacher.query().order(teachme_db.teacher.name)
        for l in teachers:
            suggestions.append(l.name+" "+l.lname)
        tags = teachme_db.tags.query().get().name if teachme_db.tags.query().get() else []
        for l in tags:
            suggestions.append(l)
        params['user'] = self.user
        params['teacher'] = self.teacher
        params['areas'] = self.areas
        params['suggestions'] = json.dumps(suggestions)
        params['shareUrl'] = self.request.url
        params['language'] = _('language')
        params['live'] = self.live
        params['company'] = self.company
        return jinja_fns.render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = fns.make_secure_val(val)
        if self.request.get("remember") == "yes":
            next_month = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%a, %d %b %Y %H:%M:%S GMT')
            self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/; expires= %s' % (name, cookie_val, next_month))
        else:
            tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
            self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/; expires= %s' % (name, cookie_val, tomorrow))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and fns.check_secure_val(cookie_val)

    def login(self, user, teacher):
        self.set_secure_cookie('usi', str(user.key.urlsafe()))
        if teacher:
            self.set_secure_cookie('tei', str(teacher.key.urlsafe()))

    def logout(self):
        self.response.headers.add_header("Set-Cookie", "usi=; Path=/")
        self.response.headers.add_header("Set-Cookie", "tei=; Path=/")

    def check_live(self):
        live = False
        channels = ['juliankmazo', 'teachmeapp']
        for channel in channels:
            if TwitchHelper.is_channel_live(channel):
                live = True
        return live

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        ukey = self.read_secure_cookie("usi")
        tkey = self.read_secure_cookie("tei")
        self.user = ukey and ndb.Key(urlsafe=ukey).get()
        self.teacher = tkey and ndb.Key(urlsafe=tkey).get()
        self.live = self.check_live()
        self.company = 'sura'
