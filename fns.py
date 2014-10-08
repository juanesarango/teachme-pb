# -*- coding: utf-8 -*-
import re
import random
import hashlib
import hmac
import datetime
import time
import unicodedata


def valid_name(name):
	USER_RE = re.compile(r"^.{3,20}$")
	return name and USER_RE.match(name)


def valid_lname(lname):
	LNAME_RE = re.compile(r"^.{3,20}$")
	return lname and LNAME_RE.match(lname)


def valid_pw(pw):
	PW_RE = re.compile(r"^.{6,20}")
	return pw and PW_RE.match(pw)


def valid_mail(mail):
	MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
	return not mail or MAIL_RE.match(mail)


def valid_register(name, lname, pw, pwcon, mail, params, have_error):
	if not valid_name(name):
		params['error_name'] = u"El nombre debe contener entre 3 y 20 caracteres sin caracteres especiales"
		have_error = True
	if not valid_lname(lname):
		params['error_lname'] = u"El apellido debe contener entre 3 y 20 caracteres sin caracteres especiales"
		have_error = True
	if not valid_pw(pw):
		params['error_pw'] = u"La contraseña debe contener entre 6 y 20 caracteres"
		have_error = True
	elif pw != pwcon:
		params['error_pwcon'] = u"La contraseña debe de coincidir"

	if not valid_mail(mail):
		params['error_mail'] = u"El e-mail está erróneo. Ejemplo: email@domain.com"
		have_error = True

	return params, have_error

########################################################
#Cookies functions


def make_secure_val(val):
	return '%s|%s' % (val, hmac.new(thing, val).hexdigest())


def check_secure_val(secure_val):
	val = secure_val.split('|')[0]
	if secure_val == make_secure_val(val):
		return val


thing = "ZaoZvf4ml3Sgn5VRsEa5gsYf4oblrku49KGwRDzn"

###############################################


def solo_dates(dt):
	dates = []
	today = datetime.datetime.now()
	for d in dt:
		if d > today:
			dates.append(str(d.year)+'-'+str(d.month)+'-'+str(d.day))
	return dates


def first_date(dt):
	fd = solo_dates(dt)
	if len(fd)>0:
		return fd[0]
	else:
		return False


def solo_hours(dt):
	hours = {}
	today = datetime.datetime.now()
	for d in dt:
		if d > today:
			if (str(d.year)+'-'+str(d.month)+'-'+str(d.day)) in hours:
				hours[str(d.year)+'-'+str(d.month)+'-'+str(d.day)].append(str(d.hour)+':'+str(minuto(d.minute)))
			else:
				hours[str(d.year)+'-'+str(d.month)+'-'+str(d.day)] = [str(d.hour)+':'+str(minuto(d.minute))]
	return hours


def minuto(m):
	if len(str(m)) == 1:
		mi = str(m)+'0'
	else:
		mi = str(m)
	return mi


def erase_past_days(days, today):
	for d in days:
		if d < today:
			days.remove(d)

	return days


def parse_areas(a):
	areas = {"matematicas" : u'Matemáticas',
			 "fisica" : u'Física',
			 "quimica" : u'Química',
			 "biologia" : u'Biología',
			 "musica" : u'Música'}
	if a in areas:
		return areas[a]
	else:
		return None


def normalise_unicode(word, lower=True):
	if isinstance(word, unicode):
		new_word = unicodedata.normalize('NFKD',word).encode('ASCII','ignore')
	else:
		new_word = word
	return new_word.lower() if lower else new_word


def alert(number):
	alertas = { 1 : ['alert-success', u'Se ha verificado tu cuenta exitosamente. Ahora a aprender!'],
				2 : ['alert-success', u'Tu información ha sido actualizada exitósamente.'],
				3 : ['alert-danger', u'Tu contraseña es inválida.'],
				4 : ['alert-warning', u'No realizaste ningun cambio.'],
				5 : ['alert-success', u'Tu pago ha sido procesado correctamente. Has agendado con éxito la sesión de clase.'],
				6 : ['alert-success', u'Has agendado con éxito la sesión de clase.'],
				7 : ['alert-danger', u'Lo sentimos. El pago ha sido rechazado. Corrige los datos de pago, o comúnicate con tu entidad financiera.'],
				8 : ['alert-danger', u'Lo sentimos, el mentor ya no cuenta con disponibilidad en esa hora. Intenta elegir una hora nueva.'],
				9 : ['alert-danger', u'Lo sentimos, la reserva no se pudo completar de manera exitosa. Inténtalo nuevamente.']
			   }
	return alertas[number]


def datetimeformat(date, utc=-5):
	now = datetime.datetime.now()
	diff = now-date
	date = date+datetime.timedelta(hours=utc)
	if diff.days<1:
		return date.strftime('%I:%M %p')
	elif diff.days<7:
		return date.strftime('%a')
	elif now.year==date.year:
		return date.strftime('%b %d')
	else:
		return date.strftime('%x')


def datetimeformatchat(date, utc=-5):
	now = datetime.datetime.now()
	diff = now-date
	date = date+datetime.timedelta(hours=utc)
	if diff.days<1:
		return date.strftime('%I:%M %p')
	else:
		return date.strftime('%m/%d, %I:%M %p')


def datetime_to_ms(base_datetime):
    # todo: fix ms resolution
    return long(time.mktime(base_datetime.timetuple()) * 1000)


def ms_to_datetime(datetime_ms):
    return datetime.datetime.fromtimestamp(datetime_ms / 1000.0)


def ms_to_date(date_ms):
    return datetime.date.fromtimestamp(date_ms / 1000.0)
