# -*- coding: utf-8 -*-
import re
import random
import hashlib
import hmac
import datetime

def valid_name(name):
	USER_RE = re.compile(r"^[a-zA-Z| ]{3,20}$")
	return name and USER_RE.match(name)

def valid_lname(lname):
	LNAME_RE = re.compile(r"^[a-zA-Z| ]{3,20}$")
	return lname and LNAME_RE.match(lname)

def valid_pw(pw):
	PW_RE = re.compile(r"^.{6,20}")
	return pw and PW_RE.match(pw)

def valid_mail(mail):
	MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
	return not mail or MAIL_RE.match(mail)

def valid_register(name, lname, pw, pwcon, mail, params, have_error):
	if not valid_name(name):
		params['error_name'] = "El nombre debe de contener entre 3 y 20 caracteres sin caracteres especiales"
		have_error = True
	if not valid_lname(lname):
		params['error_lname'] = "El apellido debe de contener entre 3 y 20 caracteres sin caracteres especiales"
		have_error = True
	if not valid_pw(pw):
		params['error_pw'] = "La contrasena debe debe de contener entre 6 y 20 caracteres"
		have_error = True
	elif pw != pwcon:
		params['error_pwcon'] = "La contrasena debe de coincidir"

	if not valid_mail(mail):
		params['error_mail'] = "El e-mail esta erroneo. Eje: email@domain.com"
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