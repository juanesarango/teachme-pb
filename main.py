# -*- coding: utf-8 -*-
import os
import webapp2
import jinja2
import math
import re
import urllib
import datetime
import json
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import mail
from google.appengine.api import images
import teachme_db
import fns
import booking
import logging

########################################################################
#Definiciones de Jinja2 para los templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)


#########################################################################
# Handler Principal
class Handler(webapp2.RequestHandler):

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		self.areas = teachme_db.areas.query().order(teachme_db.areas.name)
		params['user'] = self.user
		params['teacher'] = self.teacher
		params['areas'] = self.areas
		return render_str(template, **params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def set_secure_cookie(self, name, val):
		cookie_val = fns.make_secure_val(val)
		self.response.headers.add_header(
			'Set-Cookie',
			'%s=%s; Path=/' % (name, cookie_val))

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
		#areas = ["Matemáticas", "Física", "Química", "Biología", "Música"]
		areas = teachme_db.areas.query().order(teachme_db.areas.name)
		mentors={}
		for a in areas:
			mentors[a.key.id()] = teachme_db.teacher.query(ndb.AND(teachme_db.teacher.areas == a.key.id(), teachme_db.teacher.aceptado==True)).fetch(3)
		
		self.render("main_page.html", mentors = mentors)

class signup(Handler):
	def get(self):
		self.render("signup.html")

	def post(self):
		have_error = False
		self.name = self.request.get('name')
		self.lname = self.request.get('lname')
		self.mail = self.request.get('mail')
		self.pw = self.request.get('pw')
		self.pwcon = self.request.get('pwcon')

		params = dict(name = self.name, email = self.mail, lname = self.lname)

		params, have_error =fns.valid_register(self.name, self.lname, self.pw, self.pwcon, self.mail, params, have_error)

		if have_error:
			self.render('signup.html', **params)
		else:
			u = teachme_db.user.query(teachme_db.user.mail == self.mail).get()
			if u:
				msg = "Ese e-mail ya se ecuentra registrado."
				self.render("signup.html", error_mail = msg)
			else:
				u = teachme_db.user.register(self.name, self.lname, self.mail, self.pw)
				u.put()
				subject = u.name + u", Bienvenido a Teachme"
				html = render_str("mail_template.html", sujeto = u.name)
				mail.send_mail("info@teachmeapp.com", u.mail, subject, "", html = html)
				self.login(u, None)
				self.redirect("/")

class login(Handler):
	def get(self):
		self.render("login.html")

	def post(self):
		mail = self.request.get("mail")
		pw = self.request.get("pw")

		u = teachme_db.user.login(mail, pw)
		if u:
			t = teachme_db.teacher.query(ancestor = u.key).get()
			self.login(u, t)
			self.redirect("/")
		else:
			msg = u"El correo o la contraseña son inválidos"
			self.render("login.html", error = msg)

class logout(Handler):
	def get(self):
		self.logout()
		self.redirect('/')

class teacher(Handler):
	def get(self, id):
		mentor = ndb.Key(urlsafe = str(id)).get()
		t_areas = []
		for a in mentor.areas:
			t_areas.append(teachme_db.areas.get_by_id(int(a)).name)
		fechas = json.dumps(booking.UTCfechas(mentor.date_available))
		dates = json.dumps(fns.solo_dates(mentor.date_available))
		hours = json.dumps(fns.solo_hours(mentor.date_available))
		self.render("teacher.html", mentor = mentor, hours = hours, dates = dates, fechas = fechas, t_areas = t_areas)

	def post(self, id):
		if not self.user:
			self.abort(403)
			return
		teacher_key = ndb.Key(urlsafe=str(id)).get()
		meet = datetime.datetime.strptime(self.request.get("date-meet"), "%Y-%m-%d %H:%M")

		if meet and teacher_key:
			if booking.check_availability_mentor(teacher_key, meet) and booking.check_availability_user(self.user, meet):
				m = teachme_db.teachout(date = meet, learner = self.user.key, teacher = teacher_key.key)
				m.put()
				self.user.teachouts.append(m.key)
				self.user.date_reserved.append(m.date)
				self.user.put()
				teacher_key.teachouts.append(m.key)
				teacher_key.date_available.remove(m.date)
				teacher_key.date_reserved.append(m.date)
				teacher_key.put()
				self.redirect("/teachouts")
				return
			else:
				self.redirect("/teacher/"+ str(teacher_key.key.urlsafe()))
				return
		else:
			self.redirect("/teacher/"+ str(teacher_key.key.urlsafe()))
			return

class comparte(Handler):
	def get(self):
		areas = teachme_db.areas.query().order(teachme_db.areas.name)
		self.render("comparte.html", areas = areas)

	def post(self):
		if not self.user:
			self.abort(403)
			return
		name = self.user.name
		lname = self.user.lname
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

		t = teachme_db.teacher(name = name, lname=lname, ciudad = ciudad, pais = pais, linkedin = linkedin, areas = areas_in, about = about, aceptado = False, parent = self.user.key)
		t.put()
		self.login(self.user, t)
		self.redirect("/profile/teacher/%s" % str(t.key.id()))

class teachouts(Handler):
	def get(self):
		if not self.user:
			self.abort(403)
			return
		now = datetime.datetime.now()
		ready = datetime.timedelta(minutes = 15)
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

		touts = {}
		mentor = {}
		disable = {}
		faltan = {}
		for t in self.user.teachouts:
			touts[t] =  t.get()
			mentor[t] = touts[t].teacher.get()
			if now >= (touts[t].date-ready):
				disable[t] = False 
			else:
				disable[t] = True
				faltan[t] = str(touts[t].date - now)

		self.render("/teachouts.html", touts = touts, mentor = mentor, disable = disable, faltan = faltan, m_touts = m_touts, learner = learner, m_disable = m_disable, m_faltan = m_faltan)

class aprende(Handler):
	def get(self, ar):
		area = teachme_db.areas.get_by_id(int(ar))
		if area:
			mentors = teachme_db.teacher.query(ndb.AND(teachme_db.teacher.areas == area.key.id(), teachme_db.teacher.aceptado==True))
			self.render("aprende.html", mentors = mentors, area = area)

class profile_teacher(Handler, blobstore_handlers.BlobstoreUploadHandler):

	def get(self, te_id):
		if not self.user:
			self.abort(403)
			return
		teacher = ndb.Key(teachme_db.teacher, int(te_id), parent = self.user.key).get()
		
		if not teacher:
			self.abort(403)
			return

		t_areas = []
		for a in teacher.areas:
			t_areas.append(teachme_db.areas.get_by_id(int(a)).name)

		fechas = json.dumps(booking.UTCfechas(teacher.date_available))
		dates = json.dumps(fns.solo_dates(teacher.date_available))
		hours = json.dumps(fns.solo_hours(teacher.date_available))
		upload_url = blobstore.create_upload_url('/upload')
		self.render("profile_teacher.html", teacher = teacher, t_areas = t_areas, upload_url = upload_url, dates = dates, hours = hours, fechas = fechas)

	def post(self):
		
		te_id = self.request.get("te_id")
		teacher = ndb.Key(teachme_db.teacher, int(te_id), parent = self.user.key).get()

		profile_pic = self.get_uploads("profile_pic")
		if profile_pic:
			blob_info = profile_pic[0]
		teacher.profile_pic = blob_info.key()
		teacher.put()
		self.redirect("/profile/teacher/%s" % str(teacher.key.id()))

class calendar_teacher_add(Handler):
	def post(self):
		if not self.user:
			self.abort(403)
			return
		te_id = self.request.get("te_id")
		teacher = ndb.Key(teachme_db.teacher, int(te_id), parent = self.user.key).get()
		if not teacher:
			self.abort(403)
			return

		d = str(self.request.get("dateto"))
		if d:
			date = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M")
			repeated = booking.check_repeated_date(teacher, date)
			if repeated[0]:
				booking.erase_past_dates(teacher)
				teacher.date_available.append(date)
				sorted(teacher.date_available)
				teacher.put()

		
		self.redirect("/profile/teacher/" + str(teacher.key.id()))

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
			sender_address = "info@teachmeapp.com"
			subject = u'Contáctanos auto'
			body = "Mensaje de: "+format(name)+"""
			"""+format(text)+"""
			"""+format(email)
			mail.send_mail(sender_address, "info@teachmeapp.com", subject, body)
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

class servehandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

app = webapp2.WSGIApplication([('/', MainPage),
								('/signup', signup),
								('/login' , login),
								('/logout' , logout),
								('/teacher/([^/]+)?', teacher),
								('/comparte', comparte),
								('/teachouts', teachouts),
								('/aprende/([0-9]+)?', aprende),
								('/profile/teacher/([0-9]+)?', profile_teacher),
								('/calendar/teacher/add', calendar_teacher_add),
								('/contacto', contacto),
								('/upload', profile_teacher),
								('/tasks/teachoutsta', teachouts_sta), 
								('/serve/([^/]+)?', servehandler)
								],
								debug=True)
