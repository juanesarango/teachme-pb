# -*- coding: utf-8 -*-
import datetime
from google.appengine.ext import ndb
from google.appengine.api import mail
import teachme_db
import logging
import main
from libs.elibom import Client

def parse_24_12(hora, minuto):
	if int(hora)<=12:
		hora_12 = str(hora)
		aop = 'AM'
	else:
		hora_12 = str(int(hora)-12)
		aop = 'PM'

	if 0 <= int(minuto) < 10:
		minuto_12 = '0'+str(minuto)
	else:
		minuto_12 = str(minuto)

	return hora_12 + ':' + minuto_12 + ' ' + aop

def parse_month(month):
	m = int(month)-1
	months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
	return months[m]

def erase_past_dates(mentor):
	today = datetime.datetime.now()
	for d in mentor.date_available:
		if d<today:
			mentor.date_available.remove(d)

def UTCfechas(dates):
	today = datetime.datetime.now()
	fechas = []
	for d in sorted(dates):
		if d>today:
			#fechas.append(str(d.year)+'-'+str(d.month)+'-'+str(d.day)+' '+str(d.hour)+':'+str(d.minute)+' UTC')
			fechas.append(d.strftime("%Y-%m-%dT%H:%MZ"))

	return fechas


def check_repeated_date(mentor, dt):
	today = datetime.datetime.now()
	if dt >= today:
		if dt in mentor.date_available:
			return [False, "Fecha repetida"]
		else:
			return [True, ""]
	else:
		return [False, "Fecha anterior a la actual"]

def check_availability_mentor(mentor, dt):
	if dt in mentor.date_available and dt not in mentor.date_reserved:
		return True
	else:
		return False

def check_availability_user(user, dt):
	if dt in user.date_reserved:
		return False
	else:
		return True

def teachouts_past():
	dif = datetime.datetime.now() - datetime.timedelta(hours = 1)
	return teachme_db.teachout.query(ndb.AND(teachme_db.teachout.date<= dif, teachme_db.teachout.status == None))
	#return teachme_db.teachout.query(teachme_db.teachout.date<= dif)
def teachouts_status(touts):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M UTC")
	for t in touts:
		if t.status_mentor=="ok" and t.status_user =="ok":
			t.status = "ok"
			t.log.append(now + " El teachout ha finalizado con exito.")

		if t.status_mentor == None and t.status_user ==None:
			t.status="fail"
			t.log.append(now + " Los participantes no han atendido el teachout.")

		if t.status_mentor=="ok" and t.status_user ==None:
			t.status = "only_mentor"
			t.log.append(now + " El aprendiz no asistio al teachout.")

		if t.status_mentor == None and t.status_user =="ok":
			t.status="only_user"
			t.log.append(now + " El mentor no asistio al teachout.")
		logging.info(t.teacher)
		tout_mentor_update(t.teacher, t.key, t.date)
		tout_user_update(t.learner, t.key, t.date)
		t.put()


def tout_mentor_update(mentor, tout, date):
	m = mentor.get()
	logging.info(m)
	if tout in m.teachouts:
		m.teachouts.remove(tout)
	m.teachouts_expired.append(tout)
	# lista = []
	# for i in m.teachouts_expired:
	# 	if i not in lista:
	# 		lista.append(i)
	# m.teachouts_expired = lista
	if date in m.date_reserved:
		m.date_reserved.remove(date)
	m.put()

def tout_user_update(user, tout, date):
	u = user.get()
	if tout in u.teachouts:
		u.teachouts.remove(tout)
	u.teachouts_expired.append(tout)
	# lista = []
	# for i in u.teachouts_expired:
	# 	if i not in lista:
	# 		lista.append(i)
	# u.teachouts_expired = lista
	if date in u.date_reserved:
		u.date_reserved.remove(date)
	u.put()

def notify_sms(user, user2, method, who, date):
	#Función para enviar notificaciones de agendamiento y recordatorio por sms. 
	#method 0 para enviar notificación de agendamiento y 1 para recordatorio.
	#who 0 para mentor, 1 para user.

	msgMentor = { 0 : [u'{user} ha agendado una sesión contigo en Teachme: {date}. Mira los detalles en tu correo',
					   u'Has agendado una sesión con {user} en Teachme: {date}. Mira los detalles en tu correo'],
				  1 : [u'Recuerda que en minutos tienes una sesión con {user} en Teachme. {date}',
				  	   u'Recuerda que en minutos tienes una sesión con {user} en Teachme. {date}']}

	elibom = Client.ElibomClient('info@teachmeapp.com', 'Xw1EqiL4q0')

	if user.movil:
		try:
			response = elibom.send_message(str(user.movil), msguser[method][who].format(user = user2.name, date = date.strftime('%I:%M %p, %d %b %Y')))
			logging.info('Elibom %s, cel: %s' % (response, user.movil))
		except Client.ElibomClientExeption, e:
			logging.error(e)
	return


def teachouts_24():
	dif26 = datetime.datetime.now() + datetime.timedelta(hours = 26)
	dif24 = datetime.datetime.now() + datetime.timedelta(hours = 22)
	return teachme_db.teachout.query(ndb.AND(teachme_db.teachout.date<= dif26, teachme_db.teachout.date >dif24, teachme_db.teachout.status == None))

def teachouts_15():
	dif40 = datetime.datetime.now() + datetime.timedelta(minutes = 40)
	dif20 = datetime.datetime.now() + datetime.timedelta(minutes = 20)
	return teachme_db.teachout.query(ndb.AND(teachme_db.teachout.date<= dif40, teachme_db.teachout.date >dif20, teachme_db.teachout.status == None))

def reminder_mail(touts, rem):
	for t in touts:
		learner = t.learner.get()
		mentor = t.teacher.get()
		if rem == 24:
			falta = "24 horas"
			subject = u'Recuerda tu sesión en 24 horas'
		else:
			falta = "minutos"
			subject = u'Recuerda que tu sesión empezará pronto'
		date_user = t.date - datetime.timedelta(minutes = learner.timezoneOffset)
		date_mentor = t.date - datetime.timedelta(minutes = mentor.timezoneOffset)
		html_user = main.render_str("mail_reminder.html", para = learner, de = mentor, t = t, falta = falta, date = date_user)
		html_mentor = main.render_str("mail_reminder.html", para = mentor, de = learner, t = t, falta = falta, date = date_mentor)
		mail.send_mail("info@teachmeapp.com", learner.mail, subject, "", html = html_user)
		mail.send_mail("info@teachmeapp.com", mentor.mail, subject, "", html = html_mentor)
