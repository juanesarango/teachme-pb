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

admins = ["julian.kmazo@gmail.com", "juanes.ao@gmail.com", "naico251@gmail.com"]
#########################################################################
# Handler Principal
class Handler(webapp2.RequestHandler):

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		params['user'] = self.user
		params['teacher'] = self.teacher
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

class Areas(Handler):
	def get(self):
		if self.user:
			if self.user.mail in admins:
				areas = teachme_db.areas.query().order(teachme_db.areas.name)
				self.render("admin_areas.html", areas = areas)
				return
		self.abort(403)
		return
		
	def post(self):
		if not self.user.mail in admins:
			self.abort(403)
			return
		area = self.request.get("area")
		subarea = self.request.get("subarea")
		sid = self.request.get("sid")

		if area:
			a = teachme_db.areas(name = format(area))
			a.put()
			self.redirect("/admin/areas")
			return
		elif subarea and sid:
			s = teachme_db.areas.get_by_id(int(sid))
			s.subarea.append(format(subarea))
			s.put()
			self.redirect("/admin/areas")
			return
		else:
			error_area = "No ingresaste nada"
			error_subarea = "No ingresaste nada"
			self.render("admin_areas", error_area = error_area, error_subarea = error_subarea)
			return

class Users(Handler):
	def get(self):
		if self.user:
			if self.user.mail in admins:
				u = teachme_db.user.query().order(-teachme_db.user.date_created)
				self.render("admin_users.html", u = u)

app = webapp2.WSGIApplication([('/admin/areas', Areas),
								('/admin/users', Users)], debug=True)