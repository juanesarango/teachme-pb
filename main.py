# -*- coding: utf-8 -*-
import os
import webapp2
import jinja2
import urllib
import datetime
import json

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import mail
from google.appengine.api import images
import teachme_db
import teachme_index
import fns
import booking
import logging
import stripe

from webapp2_extras import i18n
from webapp2_extras.i18n import gettext as _
from google.appengine.ext.webapp.util import run_wsgi_app

########################################################################
#Definiciones de Jinja2 para los templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), extensions=['jinja2.ext.i18n'], autoescape=True)
jinja_env.install_gettext_translations(i18n)
jinja_env.filters['first_date'] = fns.first_date
jinja_env.filters['datetimeformat'] = fns.datetimeformat
jinja_env.filters['datetimeformatchat'] = fns.datetimeformatchat

# jinja2 config with i18n enabled
config = {'webapp2_extras.jinja2': {'template_path': 'templates', 'environment_args': {'extensions': ['jinja2.ext.i18n']}}}
AVAILABLE_LOCALES = ['es_ES', 'en_US']


def render_str(template, **params):
    j = jinja_env.get_template(template)
    return j.render(params)

#########################################################################
# Handler Principal


class Handler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        # first, try and set locale from cookie
        locale = request.cookies.get('locale')
        if locale in AVAILABLE_LOCALES:
            i18n.get_i18n().set_locale(locale)
        else:
            # if that failed, try and set locale from accept language header
            header = request.headers.get('Accept-Language', '')  # e.g. en-gb,en;q=0.8,es-es;q=0.5,eu;q=0.3
            locales = [locale.split(';')[0] for locale in header.split(',')]
            for locale in locales:
                if locale in AVAILABLE_LOCALES:
                    i18n.get_i18n().set_locale(locale)
                    break
            else:
                # if still no locale set, use the first available one
                i18n.get_i18n().set_locale(AVAILABLE_LOCALES[0])

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
        return render_str(template, **params)

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

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        ukey = self.read_secure_cookie("usi")
        tkey = self.read_secure_cookie("tei")
        self.user = ukey and ndb.Key(urlsafe=ukey).get()
        self.teacher = tkey and ndb.Key(urlsafe=tkey).get()

#########################################################################
#Pagina principal


class MainPage(Handler):
    def get(self):
        l_index = self.request.get('l')
        logging.error(l_index)
        if l_index == '1':
            logging.error('LOCALE es_ES')
            language = u"Español"
            locale = 'es_ES'
        elif l_index == '2':
            logging.error('LOCALE en_US')
            language = u"English"
            locale = 'en_US'
        else:
            locale = 'es_ES'
            language = u"Español"
        i18n.get_i18n().set_locale(locale)
        logging.error(locale)
        al = self.request.get('m')
        if al:
            alert = fns.alert(int(al))
        else:
            alert = False
        areas = teachme_db.areas.query().order(teachme_db.areas.name)
        mentors = {}
        for a in areas:
            mentors[a.key.id()] = teachme_db.teacher.query(ndb.AND(teachme_db.teacher.areas == a.key.id(), teachme_db.teacher.aceptado == True)).order(-teachme_db.teacher.rating).fetch(3)
        self.render("main_page.html", mentors=mentors, alert=alert, language=language)


class signup(Handler):
    def get(self):
        redirect = self.request.get('redirect')
        if not redirect:
            redirect = '/'
        self.render("signup.html", redirect=redirect)

    def post(self):
        have_error = False
        self.name = self.request.get('name')
        self.lname = self.request.get('lname')
        self.mail = self.request.get('mail')
        self.pw = self.request.get('pw')
        self.pwcon = self.request.get('pwcon')
        self.fbID = self.request.get('fbID')
        self.gender = self.request.get('gender')
        self.tzo = int(self.request.get('timezoneOffset'))
        redirect = self.request.get('redirect')
        params = dict(name=self.name, email=self.mail, lname=self.lname, redirect=redirect)
        if not self.fbID:
            params, have_error = fns.valid_register(self.name, self.lname, self.pw, self.pwcon, self.mail, params, have_error)
        if have_error:
            self.render('signup.html', **params)
        else:
            u = teachme_db.user.query(teachme_db.user.mail == self.mail).get()
            if u:
                if not self.fbID:
                    msg = "Ese e-mail ya se ecuentra registrado."
                    self.render("signup.html", error_mail=msg)
                elif self.fbID == u.fbID:
                    t = teachme_db.teacher.query(ancestor=u.key).get()
                    self.login(u, t)
                    self.redirect('/')
            else:
                if not self.fbID:
                    u = teachme_db.user.register(self.name, self.lname, self.mail, self.pw, self.tzo)
                else:
                    profile_pic_r = "https://graph.facebook.com/v2.1/"+str(self.fbID)+"/picture"
                    u = teachme_db.user(name=self.name, lname=self.lname, mail=self.mail, fbID=int(self.fbID), gender=self.gender, timezoneOffset=self.tzo, profile_pic_r=profile_pic_r)
                u.put()
                subject = u.name + u", Bienvenido a Teachme"
                enlace = "https://www.teachmeapp.com/user/verify/?r=" + u.key.urlsafe()
                html = render_str("mail_template.html", sujeto=u.name, enlace=enlace)
                mail.send_mail("TeachMe <info@teachmeapp.com>", u.mail, subject, "", html=html)
                self.login(u, None)
                if not redirect:
                    redirect = '/'
                self.redirect(redirect)


class login(Handler):
    def get(self):
        redirect = self.request.get('redirect')
        if not redirect:
            redirect = '/'
        self.render("login.html", redirect=redirect)

    def post(self):
        mail = self.request.get("mail")
        pw = self.request.get("pw")
        fbID = self.request.get('fbID')
        redirect = self.request.get("redirect")
        if not fbID:
            u = teachme_db.user.login(mail, pw)
        else:
            u = teachme_db.user.query(ndb.AND(teachme_db.user.mail == mail, teachme_db.user.fbID == int(fbID))).get()
        if u:
            t = teachme_db.teacher.query(ancestor=u.key).get()
            self.login(u, t)
            if redirect:
                self.redirect(redirect)
            else:
                self.redirect("/")
        else:
            msg = u"El correo o la contraseña son inválidos"
            self.render("login.html", error=msg, redirect=redirect)


class logout(Handler):
    def get(self):
        self.logout()
        self.redirect('/')


class teacher(Handler):
    def get(self, id):
        try:
            mentor = ndb.Key(urlsafe=str(id)).get()
        except:
            self.abort(404)
        al = self.request.get('m')
        if al:
            alert = fns.alert(int(al))
        else:
            alert = False
        reviews = teachme_db.review.query(ancestor=mentor.key).order(-teachme_db.review.date)
        t_areas = []
        for a in mentor.areas:
            t_areas.append(teachme_db.areas.get_by_id(int(a)))
        fechas = json.dumps(booking.UTCfechas(mentor.date_available))
        dates = json.dumps(fns.solo_dates(mentor.date_available))
        hours = json.dumps(fns.solo_hours(mentor.date_available))
        self.render("teacher.html", mentor=mentor, hours=hours, dates=dates, fechas=fechas, t_areas=t_areas, reviews=reviews, alert=alert)

    def post(self, id):
        if not self.user:
            self.abort(403)
            return
        teacher_key = ndb.Key(urlsafe=str(id)).get()
        area = self.request.get("select-area")
        tema = self.request.get("tema")
        meet_wf = self.request.get("dateMeet")
        pago = False

        # Si ingreso fecha
        if meet_wf and teacher_key:
            meet = datetime.datetime.strptime(meet_wf, "%Y-%m-%d %H:%M")
            timezoneOffset = int(self.request.get("timezoneOffset"))
            # Si la fecha no está ocupada por el mentor ni el usuario
            if booking.check_availability_mentor(teacher_key, meet) and booking.check_availability_user(self.user, meet):
                metodo = self.request.get("metodo_pago")
                # Elige el método de pago
                if metodo == "BONO":
                    codigo = self.request.get("codigo")
                    PROMOS = [
                        "PRIMERACLASE",
                        "DEMOPRUEBA"
                        ]
                    if codigo in PROMOS:
                        pago = True
                elif metodo == "STRIPE":
                    if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
                        stripe.verify_ssl_certs = False
                    # Set your secret key: remember to change this to your live secret key in production: https://dashboard.stripe.com/account
                    stripe.api_key = "sk_live_4UNYyvnaDMGTjlidSqmDbuVm"
                    token = self.request.get("stripeToken")
                    logging.info(token)
                    # Create the charge on Stripe's servers - this will charge the user's card
                    try:
                        amount = teacher_key.fee*100
                        if amount == 0:
                            amount = 3000
                        charge = stripe.Charge.create(
                            amount=amount,  # amount in cents, again
                            currency="usd",
                            card=token,
                            description=u"Sesión con " + self.request.get("mentorName"),
                            receipt_email=self.user.mail
                        )
                        pago = True
                    except stripe.CardError, e:
                        # The card has been declined
                        logging.error("FALLO PAGO")
                        pass
                # Si el pago fue exitoso
                elif metodo == "GRATIS" and teacher_key.fee == 0:
                    pago = True
                else:
                    self.abort(403)
                    return

                if pago:
                    # Crea el teachout
                    t = teachme_db.teachout(date=meet, learner=self.user.key, teacher=teacher_key.key, area=area, tema=tema)
                    t.put()
                    # Guarda info de la transacción
                    if metodo == "STRIPE":
                        factura = teachme_db.payments(parent=self.user.key, teachout=t.key, teacher=teacher_key.key, metodo=metodo, cantidad=amount, charge=charge.id)
                    else:
                        factura = teachme_db.payments(parent=self.user.key, teachout=t.key, teacher=teacher_key.key, metodo=metodo, cantidad=teacher_key.fee)
                    factura.put()

                    self.user.teachouts.append(t.key)
                    self.user.pagos.append(factura.key)
                    self.user.date_reserved.append(t.date)
                    self.user.timezoneOffset = timezoneOffset
                    self.user.put()
                    teacher_key.teachouts.append(t.key)
                    teacher_key.date_available.remove(t.date)
                    teacher_key.date_reserved.append(t.date)
                    teacher_key.put()

                    date_mentor = t.date - datetime.timedelta(minutes=teacher_key.timezoneOffset)
                    date_learner = t.date - datetime.timedelta(minutes=self.user.timezoneOffset)

                    booking.notify_sms(teacher_key, self.user, 0, 0, date_mentor)  # SMS to mentor
                    booking.notify_sms(self.user, teacher_key, 0, 1, date_learner)  # SMS to user

                    html_user = render_str("mail_booking.html", sujeto=self.user.name, mentor=teacher_key, t=t, date=date_learner)
                    html_mentor = render_str("mail_booking_mentor.html", sujeto=teacher_key.name, u=self.user, t=t, date=date_mentor)
                    subject = "Confirmación de sesión agendada"
                    mail.send_mail("TeachMe <info@teachmeapp.com>", self.user.mail, subject, "", html=html_user)
                    mail.send_mail("TeachMe <info@teachmeapp.com>", teacher_key.mail, subject, "", html=html_mentor)

                    if metodo == "GRATIS":
                        self.redirect("/teachouts?m=6")
                    self.redirect("/teachouts?m=5")
                    return
                else:
                    self.redirect("/teacher/" + str(teacher_key.key.urlsafe())+"?m=7")
                    return
            else:
                self.redirect("/teacher/" + str(teacher_key.key.urlsafe())+"?m=8")
                return
        else:
            self.redirect("/teacher/" + str(teacher_key.key.urlsafe())+"?m=9")
            return


class comparte(Handler):
    def get(self):

        if self.teacher:
            self.abort(403)
            return
        areas = teachme_db.areas.query().order(teachme_db.areas.name)
        self.render("comparte.html", areas=areas)

    def post(self):
        if not self.user:
            self.abort(403)
            return
        if self.teacher:
            self.abort(403)
            return
        name = self.user.name
        lname = self.user.lname
        mail = self.user.mail
        ciudad = self.request.get("ciudad")
        pais = self.request.get("pais")
        linkedin = self.request.get("linkedin")
        areas = teachme_db.areas.query()
        areas_in = []
        for a in areas:
            ar = self.request.get(str(a.key.id()))
            if ar:
                areas_in.append(int(ar))

        about = self.request.get("about")

        t = teachme_db.teacher(name=name, lname=lname, mail=mail, fee=0, profile_pic=self.user.profile_pic, profile_pic_r=self.user.profile_pic_r,
                               ciudad=ciudad, pais=pais, linkedin=linkedin, areas=areas_in, about=about, aceptado=False, reviews=0, rating=0,
                               timezoneOffset=self.user.timezoneOffset, parent=self.user.key)
        t.put()
        teachme_index.create_index(t)
        self.login(self.user, t)
        self.redirect("/profile/teacher/%s" % str(t.key.id()))


class teachouts(Handler):
    def get(self):
        #depurar_teachouts()

        al = self.request.get('m')
        if al:
            alert = fns.alert(int(al))
        else:
            alert = False

        if not self.user:
            self.abort(403)
            return
        now = datetime.datetime.now()
        ready = datetime.timedelta(minutes=15)
        m_touts = {}
        learner = {}
        m_disable = {}
        m_faltan = {}
        if self.teacher:
            for mt in self.teacher.teachouts:
                m_touts[mt] = mt.get()
                learner[mt] = m_touts[mt].learner.get()
                if now >= (m_touts[mt].date-ready):
                    m_disable[mt] = False
                else:
                    m_disable[mt] = True
                    m_faltan[mt] = str(m_touts[mt].date-now)

        m_etouts = {}
        elearner = {}
        if self.teacher:
            for mt in self.teacher.teachouts_expired:
                m_etouts[mt] = mt.get()
                elearner[mt] = m_etouts[mt].learner.get()

        touts = {}
        mentor = {}
        disable = {}
        faltan = {}
        for t in self.user.teachouts:
            touts[t] = t.get()
            mentor[t] = touts[t].teacher.get()
            if now >= (touts[t].date-ready):
                disable[t] = False
            else:
                disable[t] = True
                faltan[t] = str(touts[t].date - now)

        etouts = {}
        ementor = {}
        for t in self.user.teachouts_expired:
            etouts[t] = t.get()
            ementor[t] = etouts[t].teacher.get()

        self.render("/teachouts.html", touts=touts, mentor=mentor, disable=disable, faltan=faltan, m_touts=m_touts,
                    learner=learner, m_disable=m_disable, m_faltan=m_faltan, etouts=etouts, ementor=ementor, m_etouts=m_etouts, elearner=elearner, alert=alert)


class aprende(Handler):
    def get(self, ar):
        area = teachme_db.areas.query(teachme_db.areas.url == ar).get()
        if not area:
            area = teachme_db.areas.get_by_id(int(ar))
            logging.warning(area)
        if area:
            mentors = teachme_db.teacher.query(ndb.AND(teachme_db.teacher.areas == area.key.id(), teachme_db.teacher.aceptado == True)).order(-teachme_db.teacher.rating)
            self.render("aprende.html", mentors=mentors, area=area)
            return
        self.abort(500)


class terminos(Handler):
    def get(self):
        self.render("terminos.html")


class politicas(Handler):
    def get(self):
        self.render("politicas.html")


class faq(Handler):
    def get(self):
        self.render("faq.html")


class profile_teacher(Handler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self, te_id):
        if not self.user:
            self.abort(403)
            return
        teacher = ndb.Key(teachme_db.teacher, int(te_id), parent=self.user.key).get()
        if not teacher:
            self.abort(403)
            return
        reviews = teachme_db.review.query(ancestor=teacher.key).order(-teachme_db.review.date)
        fechas = json.dumps(booking.UTCfechas(teacher.date_available))
        dates = json.dumps(fns.solo_dates(teacher.date_available))
        hours = json.dumps(fns.solo_hours(teacher.date_available))
        upload_url = blobstore.create_upload_url('/upload')
        taglist = json.dumps(teachme_db.tags.query().get().name)
        self.render("profile_teacher.html", teacher=teacher, upload_url=upload_url, dates=dates, hours=hours, fechas=fechas, taglist=taglist, reviews=reviews)

    def post(self):
        te_id = self.request.get("te_id")
        teacher = ndb.Key(teachme_db.teacher, int(te_id), parent=self.user.key).get()
        profile_pic = self.get_uploads("profile_pic")
        if profile_pic:
            blob_info = profile_pic[0]
            if teacher.profile_pic:
                if teacher.profile_pic_r:
                    images.delete_serving_url(teacher.profile_pic)
                blobstore.delete(teacher.profile_pic)
            teacher.profile_pic = blob_info.key()
            teacher.profile_pic_r = images.get_serving_url(teacher.profile_pic, size=200, secure_url=True)
            self.user.profile_pic = blob_info.key()
            self.user.profile_pic_r = teacher.profile_pic_r
            teacher.put()
            self.user.put()
        self.redirect("/profile/teacher/%s" % str(teacher.key.id()))


class editabout(Handler):
    def post(self):
        if not self.user and not self.teacher:
            self.abort(403)
        about = self.request.get("editabout")
        fee = self.request.get("fee")
        fn = self.request.get("fn")
        if about:
            self.teacher.about = about
        if fee:
            self.teacher.fee = int(fee)
        areas = teachme_db.areas.query()
        if fn == "editAreas":
            for a in areas:
                ar = self.request.get(str(a.key.id()))
                if ar:
                    if int(ar) not in self.teacher.areas:
                        self.teacher.areas.append(int(ar))
                else:
                    if a.key.id() in self.teacher.areas:
                        self.teacher.areas.remove(a.key.id())
        self.teacher.put()
        if fn == "editAreas":
            teachme_index.create_index(self.teacher)

        self.redirect("/profile/teacher/%s" % self.teacher.key.id())


class msg2mentor(Handler):
    def post(self):
        if not self.user:
            self.abort(403)
        mensaje = self.request.get("message")
        teacher_key = self.request.get("teacher_key")

        if mensaje and teacher_key:
            teacher = ndb.Key(urlsafe=str(teacher_key)).get()
            m = teachme_db.msg(mFrom=self.user.key, mTo=teacher.key.parent(), mensaje=mensaje)
            m.put()
            c = teachme_db.chat(parent=self.user.key, teacher=teacher.key, msgs=[m])
            c.put()
            html_mail = render_str("mail_question.html", para=teacher, de=self.user, m=m, chat=c.key.urlsafe())
            mail.send_mail(sender="TeachMe Pregunta <info@teachmeapp.com>", to=teacher.mail, subject=self.user.name+" de Teachme te ha hecho una pregunta", body="", html=html_mail)
            self.redirect("/teacher/%s" % teacher_key)
        else:
            self.redirect("/")


class reply(Handler):
    def get(self):
        r = self.request.get("r")
        msg = ndb.Key(urlsafe=str(r)).get()
        c = self.request.get("c")
        #chat = ndb.Key(urlsafe=str(c)).get()
        learner = msg.mFrom.get()
        teacher = msg.mTo.get()
        fecha = msg.created
        self.render("responder.html", mentor=teacher, learner=learner, mensaje=msg.mensaje, fecha=fecha, msg=r, chat=c)

    def post(self):
        newMsg = self.request.get("replyMsg")
        msgKey = self.request.get("msgKey")
        chatKey = self.request.get("chatKey")
        msg = ndb.Key(urlsafe=str(msgKey)).get()
        chat = ndb.Key(urlsafe=str(chatKey)).get()

        if not newMsg:
            e_replyMsg = "No has escrito ningún mensaje para responder"
            self.render("responder.html", mentor=msg.teacher, learner=msgKey.parent().get(), mensaje=msg.mensaje, fecha=msg.created,
                        msg=msgKey.urlsafe(), chat=chatKey.urlsafe(), e_replyMsg=e_replyMsg)
            return
        else:
            m = teachme_db.msg(mFrom=msg.mTo, mTo=msg.mFrom, mensaje=newMsg)
            m.put()
            chat.msgs.append(m)
            chat.put()
            mFrom = msg.mFrom.get()
            mTo = msg.mTo.get()
            html_mail = render_str("mail_reply.html", para=mFrom, de=mTo, m=m, p=msg, chat=chat.key.urlsafe())
            mail.send_mail(sender="TeachMe Respuesta<info@teachmeapp.com>", to=mFrom.mail, subject=mTo.name + " de Teachme ha respondido tu pregunta", body="", html=html_mail)
            self.redirect("/")


class addtags(Handler):
    def post(self):
        tags = teachme_db.tags.query().get()
        te_id = self.request.get("te_id")
        if te_id:
            new_tag = self.request.get("new_tags")
            if new_tag:
                teacher = ndb.Key(teachme_db.teacher, int(te_id), parent=self.user.key).get()
                if new_tag not in teacher.tags:
                    teacher.tags.append(new_tag)
                    teacher.put()
                    teachme_index.create_index(teacher)
                    if new_tag not in tags.name:
                        logging.info(new_tag)
                        tags.name.append(new_tag)
                        tags.put()
        else:
            re_id = self.request.get("re_id")
            if re_id:
                teacher = ndb.Key(teachme_db.teacher, int(re_id), parent=self.user.key).get()
                tag_r = self.request.get("tag_r")
                if tag_r:
                    teacher.tags.remove(tag_r)
                    teacher.put()
                    teachme_index.create_index(teacher)
                    te_id = re_id
        self.redirect("/profile/teacher/%s" % te_id)


class calendar_teacher_add(Handler):
    def post(self):
        if not self.user:
            self.abort(403)
            return
        te_id = self.request.get("te_id")
        teacher = ndb.Key(teachme_db.teacher, int(te_id), parent=self.user.key).get()
        if not teacher:
            self.abort(403)
            return
        for i in range(24):
            d = str(self.request.get(str(i)))
            if d:
                date = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M")
                repeated = booking.check_repeated_date(teacher, date)
                if repeated[0]:
                    booking.erase_past_dates(teacher)
                    teacher.date_available.append(date)
                    sorted(teacher.date_available)
        timezoneOffset = self.request.get('timezoneOffset')
        if timezoneOffset:
            teacher.timezoneOffset = int(timezoneOffset)
        teacher.put()
        self.redirect("/profile/teacher/" + str(teacher.key.id()))


class calificar(Handler):
    def post(self):
        if not self.user:
            self.abort(403)
            return
        reviewRating = int(self.request.get("reviewRating"))
        reviewComment = self.request.get("reviewComment")
        reviewTout = ndb.Key(urlsafe=self.request.get("reviewTout")).get()
        reviewMentor = ndb.Key(urlsafe=self.request.get("reviewMentor")).get()
        #reviewUser = self.user
        if reviewRating and reviewTout and reviewMentor:
            r = teachme_db.review(rating=reviewRating, comment=reviewComment, user=self.user.key, teachout=reviewTout.key, parent=reviewMentor.key)
            r.put()
            reviewMentor.rating = ((reviewMentor.rating*reviewMentor.reviews)+reviewRating)/(reviewMentor.reviews+1)
            reviewMentor.reviews += 1
            reviewMentor.put()
            reviewTout.rating = reviewRating
            reviewTout.review = r.key
            reviewTout.put()
            self.redirect("/teachouts")
        else:
            msg = "Ingresa tu calificación"
            self.render("/teachouts.html", msg=msg)


class contacto(Handler):
    def get(self):
        self.render("contacto.html")

    def post(self):
        name = self.request.get("name")
        email = self.request.get("email")
        text = self.request.get("text")
        if not email:
            email = " "
        if name and text:
            sender_address = "TeachMe <info@teachmeapp.com>"
            subject = u'Contáctanos auto'
            body = "Mensaje de: "+format(name)+"""
            """+format(text)+"""
            """+format(email)
            mail.send_mail(sender_address, "TeachMe <info@teachmeapp.com>", subject, body)
            e_text = "Gracias por tomarte el tiempo de escribirnos :)"
            self.render("contacto.html", e_text=e_text)
            return
        else:
            e_text = "Escribe tu nombre y un texto para enviar."
            self.render("contacto.html", e_text=e_text, name=name, email=email, text=text)


class teachouts_sta(Handler):
    def get(self):
        t = booking.teachouts_past()
        booking.teachouts_status(t)


class reminder_mailing_24(Handler):
    def get(self):
        t24 = booking.teachouts_24()
        booking.reminder_mail(t24, 24)


class reminder_mailing_15(Handler):
    def get(self):
        t15 = booking.teachouts_15()
        booking.reminder_mail(t15, 15)


class sitemap(Handler):
    def get(self):
        self.render("sitemap.xml")


class servehandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)


class manualtask(Handler):
    def get(self):
        self.response.out.write("ok")


class buscar(Handler):
    def get(self):
        query_string = self.request.get("q")
        results = teachme_index.make_query(fns.normalise_unicode(query_string))
        if results:
            number_returned = len(results.results)
            mentors = []
            for docs in results:
                mentors.append(ndb.Key(urlsafe=docs.fields[5].value).get())
            self.render("search_results.html", results=results, mentors=mentors, number_returned=number_returned, query_string=query_string)

    def post(self):
        query_string = self.request.get("q")
        results = teachme_index.make_query(fns.normalise_unicode(query_string))
        if results:
            number_returned = len(results.results)
            mentors = []
            for docs in results:
                mentors.append(ndb.Key(urlsafe=docs.fields[5].value).get())
            self.render("search_results.html", results=results, mentors=mentors, number_returned=number_returned, query_string=query_string)
        else:
            self.redirect("/")


class user_verify(Handler):
    def get(self):
        ukey = self.request.get('r')
        user = ndb.Key(urlsafe=str(ukey)).get()
        if user:
            user.verificate = True
            user.put()
            self.redirect('/?m=1')


class language(Handler):
    def post(self):
        locale = self.request.get('locale')
        if locale in self.AVAILABLE_LOCALES:
            self.response.set_cookie('locale', locale, max_age=15724800)  # 26 weeks' worth of seconds

        # redirect to referrer or root
        url = self.request.headers.get('Referer', '/')
        self.redirect(url)


class account(Handler):
    def get(self):
        if not self.user:
            self.abort(403)
            return
        al = self.request.get('m')
        if al:
            alert = fns.alert(int(al))
        else:
            alert = False
        self.render("account.html", alert=alert)

    def post(self):
        if not self.user:
            self.abort(403)
            return
        name = self.request.get("name")
        lname = self.request.get("lname")
        oldpw = self.request.get("oldpw")
        newpw = self.request.get("newpw")
        movil = self.request.get("movil")
        update = False
        updatenpw = False

        if self.user.name != name:
            self.user.name = name
            if self.teacher:
                self.teacher.name = name
            update = True
            updatenpw = True
        if self.user.lname != lname:
            self.user.lname = lname
            if self.teacher:
                self.teacher.lname = lname
            update = True
            updatenpw = True
        if movil and self.user.movil != movil:
            self.user.movil = int(movil)
            if self.teacher:
                self.teacher.movil = int(movil)
            update = True
            updatenpw = True
        if newpw:
            if teachme_db.valid_pw(self.user.mail, oldpw, self.user.pw_hash):
                self.user.pw_hash = teachme_db.make_pw_hash(self.user.mail, newpw)
                update = True
            else:
                self.redirect('/account?m=3')
                return
        if update:
            self.user.put()
            if self.teacher and updatenpw:
                self.teacher.put()
            self.redirect('/account?m=2')
        else:
            self.redirect('/account?m=4')


class messages(Handler):
    def get(self):
        if not self.user:
            self.abort(403)
            return
        al = self.request.get('m')
        if al:
            alert = fns.alert(int(al))
        else:
            alert = False

        number_chat = self.request.get("n")
        if not number_chat:
            number_chat = 1
        else:
            number_chat = int(number_chat)
        teacher = self.user.is_teacher()
        chats = teachme_db.chat.query(ancestor=self.user.key).fetch()
        if teacher:
            chats2 = teachme_db.chat.query(teachme_db.chat.teacher == teacher.key).fetch()
            for c in chats2:
                if c not in chats:
                    chats.append(c)
        chats.sort(key=lambda x: x.msgs[-1].created, reverse=True)
        # chats=[]
        self.render("messages.html", alert=alert, chats=chats, number=number_chat)

    def post(self):
        if not self.user:
            self.abort(403)
            return
        chatkey = self.request.get("chatkey")
        chat = ndb.Key(urlsafe=str(chatkey)).get()

        mensaje = self.request.get("mensaje")
        if mensaje:
            if self.user.key == chat.teacher.parent():
                mTo = chat.key.parent()
            elif self.user.key == chat.key.parent():
                mTo = chat.teacher.parent()
            m = teachme_db.msg(mFrom=self.user.key, mTo=mTo, mensaje=mensaje)
            m.put()
            chat.msgs.append(m)
            chat.put()

        number_chat = int(self.request.get("n"))
        self.redirect('/messages?n=' + str(number_chat))


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/language', language),
                               ('/signup', signup),
                               ('/login', login),
                               ('/logout', logout),
                               ('/buscar/', buscar),
                               ('/teacher/([^/]+)?', teacher),
                               ('/user/verify/', user_verify),
                               ('/comparte', comparte),
                               ('/teachouts', teachouts),
                               ('/aprende/([\w-]+)?', aprende),
                               ('/profile/teacher/([0-9]+)?', profile_teacher),
                               ('/account', account),
                               ('/messages', messages),
                               ('/editabout', editabout),
                               ('/msg2mentor', msg2mentor),
                               ('/reply/', reply),
                               ('/addtags', addtags),
                               ('/calendar/teacher/add', calendar_teacher_add),
                               ('/terminos', terminos),
                               ('/politicas', politicas),
                               ('/faq', faq),
                               ('/contacto', contacto),
                               ('/upload', profile_teacher),
                               ('/calificar', calificar),
                               ('/tasks/teachoutsta', teachouts_sta),
                               ('/tasks/manualtask', manualtask),
                               ('/tasks/remindermailing24', reminder_mailing_24),
                               ('/tasks/remindermailing15', reminder_mailing_15),
                               ('/sitemap.xml', sitemap),
                               ('/serve/([^/]+)?', servehandler)
                               ], debug=True, config=config)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
