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
import stripe
import ssl
#import stripe
#import ssl

########################################################################
#Definiciones de Jinja2 para los templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)



def render_str(template, **params):
	j = jinja_env.get_template(template)
	return j.render(params)

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
		
		if self.request.get("remember")=="yes":
			next_month = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%a, %d %b %Y %H:%M:%S GMT')
			self.response.headers.add_header('Set-Cookie','%s=%s; Path=/; expires= %s' % (name, cookie_val, next_month))
			#self.response.headers.add_header('Set-Cookie','%s=%s; Path=/' % (name, cookie_val))
		else:
			tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
			self.response.headers.add_header('Set-Cookie','%s=%s; Path=/; expires= %s' % (name, cookie_val, tomorrow))
		 
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
		redirect = self.request.get('redirect')
		if not redirect:
			redirect = '/'
		self.render("signup.html", redirect = redirect)

	def post(self):
		have_error = False
		self.name = self.request.get('name')
		self.lname = self.request.get('lname')
		self.mail = self.request.get('mail')
		self.pw = self.request.get('pw')
		self.pwcon = self.request.get('pwcon')
		redirect = self.request.get('redirect')

		params = dict(name = self.name, email = self.mail, lname = self.lname, redirect= redirect)

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
				enlace = "https://www.teachmeapp.com/verify/user/" + u.key.urlsafe()
				html = render_str("mail_template.html", sujeto = u.name, enlace = enlace)
				mail.send_mail("info@teachmeapp.com", u.mail, subject, "", html = html)
				self.login(u, None)
				self.redirect(redirect)

class login(Handler):
	def get(self):
		redirect = self.request.get('redirect')
		if not redirect:
			redirect = '/'
		self.render("login.html", redirect= redirect)

	def post(self):
		mail = self.request.get("mail")
		pw = self.request.get("pw")
		redirect = self.request.get("redirect")

		u = teachme_db.user.login(mail, pw)
		if u:
			t = teachme_db.teacher.query(ancestor = u.key).get()
			self.login(u, t)
			if redirect:
				self.redirect(redirect)
			else:
				self.redirect("/")
		else:
			msg = u"El correo o la contraseña son inválidos"
			self.render("login.html", error = msg, redirect = redirect)

class logout(Handler):
	def get(self):
		self.logout()
		self.redirect('/')

class teacher(Handler):
	def get(self, id):
		try:
			mentor = ndb.Key(urlsafe = str(id)).get()
		except:
			self.abort(404)
		flag = self.request.get("t")
		reviews = teachme_db.review.query(ancestor = mentor.key).order(-teachme_db.review.date)
		t_areas = []
		for a in mentor.areas:
			t_areas.append(teachme_db.areas.get_by_id(int(a)))
		fechas = json.dumps(booking.UTCfechas(mentor.date_available))
		dates = json.dumps(fns.solo_dates(mentor.date_available))
		hours = json.dumps(fns.solo_hours(mentor.date_available))
		self.render("teacher.html", mentor = mentor, hours = hours, dates = dates, fechas = fechas, t_areas = t_areas, reviews = reviews, flag= flag)

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
					logging.error(token)
					# Create the charge on Stripe's servers - this will charge the user's card
					try:
						amount = teacher_key.fee*100
						if amount == 0:
							amount = 3000
					 	charge = stripe.Charge.create(
					    	amount=amount, # amount in cents, again
					     	currency="usd",
					     	card=token,
					    	description= u"Sesión con " + self.request.get("mentorName"),
					    	receipt_email = self.user.mail
					  	)
					  	pago = True
					except stripe.CardError, e:
					  	# The card has been declined
					  	logging.error("FALLO PAGO")
					  	pass
				# Si el pago fue exitoso
				elif metodo == "GRATIS" and teacher_key.fee==0:
					pago = True
				else:
					self.abort(403)
					return

				if pago ==True:
					# Crea el teachout
					t = teachme_db.teachout(date = meet, learner = self.user.key, teacher = teacher_key.key, area = area, tema = tema)
					t.put()
					# Guarda info de la transacción
					if metodo =="STRIPE":
						factura = teachme_db.payments(parent = self.user.key, teachout = t.key, teacher = teacher_key.key, metodo = metodo, cantidad = amount, charge = charge.id )			
					else:
						factura = teachme_db.payments(parent = self.user.key, teachout = t.key, teacher = teacher_key.key, metodo = metodo, cantidad = teacher_key.fee)
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

					date_mentor = t.date - datetime.timedelta(minutes = teacher_key.timezoneOffset)
					date_learner = t.date - datetime.timedelta(minutes = self.user.timezoneOffset)

					html_user = render_str("mail_booking.html", sujeto = self.user.name, mentor = teacher_key, t = t, date = date_learner)
					html_mentor = render_str("mail_booking_mentor.html", sujeto = teacher_key.name, u = self.user, t = t, date = date_mentor)
					subject = "Confirmación de sesión agendada"
					mail.send_mail("info@teachmeapp.com", self.user.mail, subject, "", html = html_user)
					mail.send_mail("info@teachmeapp.com", teacher_key.mail, subject, "", html = html_mentor)

					if metodo== "GRATIS":
						self.redirect("/teachouts")
					self.redirect("/teachouts?t=SUCCEED")
					return
				else:
					self.redirect("/teacher/"+ str(teacher_key.key.urlsafe())+"?t=FAILED")
					return
			else:
				self.redirect("/teacher/"+ str(teacher_key.key.urlsafe())+"?t=FAILED")
				return
		else:
			self.redirect("/teacher/"+ str(teacher_key.key.urlsafe())+"?t=FAILED")
			return

class comparte(Handler):
	def get(self):
		if self.teacher:
			self.abort(403)
			return
		areas = teachme_db.areas.query().order(teachme_db.areas.name)
		self.render("comparte.html", areas = areas)

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

		t = teachme_db.teacher(name = name, lname=lname, mail = mail, fee = 0, ciudad = ciudad, pais = pais, linkedin = linkedin, areas = areas_in, about = about, aceptado = False, reviews=0, rating=0, parent = self.user.key)
		t.put()
		self.login(self.user, t)
		self.redirect("/profile/teacher/%s" % str(t.key.id()))

class teachouts(Handler):
	def get(self):
		#depurar_teachouts()
		flag = self.request.get("t")
		logging.error("FLAG: "+flag)
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
			touts[t] =  t.get()
			mentor[t] = touts[t].teacher.get()
			if now >= (touts[t].date-ready):
				disable[t] = False 
			else:
				disable[t] = True
				faltan[t] = str(touts[t].date - now)

		etouts = {}
		ementor = {}
		for t in self.user.teachouts_expired:
			etouts[t]= t.get()
			ementor[t] = etouts[t].teacher.get()

		self.render("/teachouts.html", touts = touts, mentor = mentor, disable = disable, faltan = faltan, m_touts = m_touts, learner = learner, m_disable = m_disable, m_faltan = m_faltan, etouts = etouts, ementor=ementor, m_etouts= m_etouts, elearner=elearner, flag=flag)

class aprende(Handler):
	def get(self, ar):
		area = teachme_db.areas.get_by_id(int(ar))
		if area:
			mentors = teachme_db.teacher.query(ndb.AND(teachme_db.teacher.areas == area.key.id(), teachme_db.teacher.aceptado==True))
			self.render("aprende.html", mentors = mentors, area = area)

class terminos(Handler):
	def get(self):
		self.render("terminos.html")

class politicas(Handler):
	def get(self):
		self.render("politicas.html")

class faq(Handler):
	def get(self):
		self.render("terminos.html")

class profile_teacher(Handler, blobstore_handlers.BlobstoreUploadHandler):

	def get(self, te_id):
		if not self.user:
			self.abort(403)
			return
		teacher = ndb.Key(teachme_db.teacher, int(te_id), parent = self.user.key).get()
		
		if not teacher:
			self.abort(403)
			return

		# t_areas = []
		# for a in teacher.areas:
		# 	t_areas.append(teachme_db.areas.get_by_id(int(a)).name)
		reviews = teachme_db.review.query(ancestor = teacher.key).order(-teachme_db.review.date)
		fechas = json.dumps(booking.UTCfechas(teacher.date_available))
		dates = json.dumps(fns.solo_dates(teacher.date_available))
		hours = json.dumps(fns.solo_hours(teacher.date_available))
		upload_url = blobstore.create_upload_url('/upload')
		taglist = json.dumps(teachme_db.tags.query().get().name)
		self.render("profile_teacher.html", teacher = teacher, upload_url = upload_url, dates = dates, hours = hours, fechas = fechas, taglist= taglist, reviews = reviews)

	def post(self):
		
		te_id = self.request.get("te_id")
		teacher = ndb.Key(teachme_db.teacher, int(te_id), parent = self.user.key).get()

		profile_pic = self.get_uploads("profile_pic")
		if profile_pic:
			blob_info = profile_pic[0]
			if teacher.profile_pic:
				if teacher.profile_pic_r:
					images.delete_serving_url(teacher.profile_pic)
				blobstore.delete(teacher.profile_pic)
			teacher.profile_pic = blob_info.key()
			teacher.profile_pic_r = images.get_serving_url(teacher.profile_pic, size = 140, secure_url=True)
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

		self.redirect("/profile/teacher/%s" % self.teacher.key.id())

class addtags(Handler):
	def post(self):
		tags = teachme_db.tags.query().get()
		te_id = self.request.get("te_id")
		if te_id:
			new_tag = self.request.get("new_tags")
			if new_tag:
				teacher = ndb.Key(teachme_db.teacher, int(te_id), parent = self.user.key).get()
				if  new_tag not in teacher.tags:
					teacher.tags.append(new_tag)
					teacher.put()
					if new_tag not in tags.name:
						logging.error(new_tag)
						tags.name.append(new_tag)
						tags.put()
		else:
			re_id = self.request.get("re_id")
			if re_id:
				teacher = ndb.Key(teachme_db.teacher, int(re_id), parent = self.user.key).get()
				tag_r = self.request.get("tag_r")
				if tag_r:
					teacher.tags.remove(tag_r)
					teacher.put()
					te_id = re_id
		self.redirect("/profile/teacher/%s" % te_id)

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
		for i in range(24):
			d = str(self.request.get(str(i)))
			if d:
				date = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M")
				repeated = booking.check_repeated_date(teacher, date)
				if repeated[0]:
					booking.erase_past_dates(teacher)
					teacher.date_available.append(date)
					sorted(teacher.date_available)
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
		reviewUser = self.user

		if reviewRating and reviewTout and reviewMentor:
			r = teachme_db.review(rating = reviewRating, comment = reviewComment, user = self.user.key, teachout = reviewTout.key, parent = reviewMentor.key)
			r.put()

			reviewMentor.rating = ((reviewMentor.rating*reviewMentor.reviews)+reviewRating)/(reviewMentor.reviews+1)
			reviewMentor.reviews +=1
			reviewMentor.put()

			reviewTout.rating = reviewRating
			reviewTout.review = r.key
			reviewTout.put()
			self.redirect("/teachouts")
		else:
			msg = "Ingresa tu calificación"
			self.render("/teachouts.html", msg = msg)
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

class reminder_mailing_24(Handler):
	def get(self):
		t24 = booking.teachouts_24()
		booking.reminder_mail(t24, 24)

class reminder_mailing_15(Handler):
	def get(self):
		t15 = booking.teachouts_15()
		booking.reminder_mail(t15, 15)

class servehandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

class manualtask(Handler):
	def get(self):
		mentors = teachme_db.teacher.query()
		for m in mentors:
			if m.profile_pic_r:
				images.delete_serving_url(m.profile_pic)
				m.profile_pic_r = images.get_serving_url(m.profile_pic, size = 140, secure_url=True)
				m.put()

		self.response.out.write("ok")

app = webapp2.WSGIApplication([('/', MainPage),
								('/signup', signup),
								('/login' , login),
								('/logout' , logout),
								('/teacher/([^/]+)?', teacher),
								('/comparte', comparte),
								('/teachouts', teachouts),
								('/aprende/([0-9]+)?', aprende),
								('/profile/teacher/([0-9]+)?', profile_teacher),
								('/editabout', editabout),
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
								('/serve/([^/]+)?', servehandler)
								],
								debug=True)
