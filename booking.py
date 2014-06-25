import datetime
from google.appengine.ext import ndb
import teachme_db

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
			fechas.append(str(d.year)+'-'+str(d.month)+'-'+str(d.day)+' '+str(d.hour)+':'+str(d.minute)+' UTC')

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
	return teachme_db.teachout.query(teachme_db.teachout.date<= dif)

def teachouts_status(touts):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M UTC")
	for t in touts:
		if t.status_mentor=="ok" and t.status_user =="ok":
			t.status = "ok"
			t.log.append(now + " El teachout ha finalizado con exito.")
			t.put()
			tout_mentor_ok(t.teacher, t.key, t.date)
			tout_user_ok(t.learner, t.key, t.date)
			

		if t.status_mentor == None and t.status_user ==None:
			t.status="fail"
			t.log.append(now + " Los participantes no han atendido el teachout.")
			t.put()
			tout_mentor_fail(t.teacher, t.key, t.date)
			tout_user_fail(t.learner, t.key, t.date)

def tout_mentor_ok(mentor, tout, date):
	m = mentor.get()
	m.teachouts.remove(tout)
	m.teachout_given.append(tout)
	if date in m.date_reserved:
		m.date_reserved.remove(date)
	m.put()

def tout_user_ok(user, tout, date):
	u = user.get()
	u.teachouts.remove(tout)
	u.teachout_attended(tout)
	if date in u.date_reserved:
		u.date_reserved.remove(date)
	u.put()

def tout_mentor_fail(mentor, tout, date):
	m = mentor.get()
	if tout in m.teachouts:
		m.teachouts.remove(tout)
	m.teachout_notgiven.append(tout)
	if date in m.date_reserved:
		m.date_reserved.remove(date)
	m.put()

def tout_user_fail(user, tout, date):
	u = user.get()
	if tout in u.teachouts:
		u.teachouts.remove(tout)
	u.teachout_notattended.append(tout)
	if date in u.date_reserved:
		u.date_reserved.remove(date)
	u.put()