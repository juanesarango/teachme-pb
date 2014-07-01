from google.appengine.ext import ndb
import random
import hashlib
from string import letters

def make_salt(length = 7):
	return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
	salt = h.split(',')[0]
	return h == make_pw_hash(name, password, salt)

class user(ndb.Model):
	name = ndb.StringProperty(required = True)
	lname = ndb.StringProperty(required = True)
	mail = ndb.StringProperty(required = True)
	pw_hash = ndb.StringProperty(required = True, indexed = False)
	date_created = ndb.DateTimeProperty(auto_now_add = True)
	profile_pic = ndb.BlobKeyProperty()
	profile_pic_r = ndb.StringProperty()

	teachouts = ndb.KeyProperty(repeated = True, kind = "teachout")
	teachouts_expired = ndb.KeyProperty(repeated = True, kind = "teachout")
	
	date_reserved = ndb.DateTimeProperty(repeated = True)

	@classmethod
	def register(cls, name, lname, mail, pw):
		pw_hash = make_pw_hash(mail, pw)
		return user(name = name, lname = lname, mail = mail, pw_hash = pw_hash)

	@classmethod
	def login(cls, mail, pw):
		u = cls.query(cls.mail == mail).get()
		if u and valid_pw(mail, pw, u.pw_hash):
			return u

class teacher(ndb.Model):
	name = ndb.StringProperty()
	lname = ndb.StringProperty()
	mail = ndb.StringProperty()
	about = ndb.TextProperty()
	profile_pic = ndb.BlobKeyProperty()
	profile_pic_r = ndb.StringProperty()
	ciudad = ndb.StringProperty()
	pais = ndb.StringProperty()
	idiomas = ndb.StringProperty(repeated = True)
	linkedin = ndb.StringProperty()
	areas = ndb.IntegerProperty(repeated = True)
	subareas = ndb.StringProperty(repeated = True)
	date_created = ndb.DateTimeProperty(auto_now_add = True)

	date_available = ndb.DateTimeProperty(repeated = True)
	date_reserved = ndb.DateTimeProperty(repeated = True)

	teachouts = ndb.KeyProperty(repeated = True, kind = "teachout")
	teachouts_expired = ndb.KeyProperty(repeated = True, kind = "teachout")

	aceptado = ndb.BooleanProperty()

class areas(ndb.Model):
	name = ndb.StringProperty(required = True)
	subarea = ndb.StringProperty(repeated = True)

class teachout(ndb.Model):
	date = ndb.DateTimeProperty()
	learner = ndb.KeyProperty(kind = user)
	teacher = ndb.KeyProperty(kind = teacher)
	cost = ndb.IntegerProperty()
	area = ndb.IntegerProperty()
	date_created = ndb.DateTimeProperty(auto_now_add = True)
	temas = ndb.TextProperty()

	status = ndb.StringProperty()
	status_mentor = ndb.StringProperty()
	status_user = ndb.StringProperty()

	log = ndb.StringProperty(repeated = True)


	
