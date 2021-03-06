from google.appengine.ext import ndb
import random
import hashlib
from string import letters


def make_salt(length=7):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


class teacher(ndb.Model):
    name = ndb.StringProperty()
    lname = ndb.StringProperty()
    mail = ndb.StringProperty()
    about = ndb.TextProperty()
    fee = ndb.IntegerProperty()
    profile_pic = ndb.BlobKeyProperty()
    profile_pic_r = ndb.StringProperty()
    ciudad = ndb.StringProperty()
    pais = ndb.StringProperty()
    idiomas = ndb.StringProperty(repeated=True)
    linkedin = ndb.StringProperty()
    areas = ndb.IntegerProperty(repeated=True)
    subareas = ndb.StringProperty(repeated=True)
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    timezoneOffset = ndb.IntegerProperty()
    tags = ndb.StringProperty(repeated=True)

    date_available = ndb.DateTimeProperty(repeated=True)
    date_reserved = ndb.DateTimeProperty(repeated=True)

    teachouts = ndb.KeyProperty(repeated=True, kind="teachout")
    teachouts_expired = ndb.KeyProperty(repeated=True, kind="teachout")

    rating = ndb.FloatProperty()
    reviews = ndb.IntegerProperty()
    score = ndb.FloatProperty()

    aceptado = ndb.BooleanProperty()

    movil = ndb.IntegerProperty()


class user(ndb.Model):
    name = ndb.StringProperty(required=True)
    lname = ndb.StringProperty(required=True)
    mail = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(indexed=False)
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    profile_pic = ndb.BlobKeyProperty()
    profile_pic_r = ndb.StringProperty()
    timezoneOffset = ndb.IntegerProperty()
    fbID = ndb.IntegerProperty()
    gender = ndb.StringProperty()
    movil = ndb.IntegerProperty()

    verificate = ndb.BooleanProperty()

    teachouts = ndb.KeyProperty(repeated=True, kind="teachout")
    teachouts_expired = ndb.KeyProperty(repeated=True, kind="teachout")

    date_reserved = ndb.DateTimeProperty(repeated=True)

    pagos = ndb.KeyProperty(repeated=True, kind="payments")

    @classmethod
    def register(cls, name, lname, mail, pw, tzo):
        pw_hash = make_pw_hash(mail, pw)
        return user(name=name, lname=lname, mail=mail, pw_hash=pw_hash, timezoneOffset=tzo)

    @classmethod
    def login(cls, mail, pw):
        u = cls.query(cls.mail == mail).get()
        if u and valid_pw(mail, pw, u.pw_hash):
            return u

    def is_teacher(self):
        t = teacher.query(ancestor=self.key).get()
        if t:
            return t
        else:
            return None

    @classmethod
    def get_by_email(cls, email=None):
        if email:
            return cls.query(cls.mail == email).get()


class areas(ndb.Model):
    name = ndb.StringProperty(required=True)
    subarea = ndb.StringProperty(repeated=True)
    url = ndb.StringProperty()
    namet = ndb.StringProperty()


class tags(ndb.Model):
    name = ndb.StringProperty(repeated=True)


class teachout(ndb.Model):
    date = ndb.DateTimeProperty()
    learner = ndb.KeyProperty(kind=user)
    teacher = ndb.KeyProperty(kind=teacher)
    cost = ndb.IntegerProperty()
    area = ndb.StringProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    tema = ndb.TextProperty()

    status = ndb.StringProperty()
    status_mentor = ndb.StringProperty()
    status_user = ndb.StringProperty()

    log = ndb.StringProperty(repeated=True)

    rating = ndb.IntegerProperty()
    review = ndb.KeyProperty(kind="review")


class review(ndb.Model):
    rating = ndb.IntegerProperty(required=True)
    comment = ndb.StringProperty()
    user = ndb.KeyProperty(required=True, kind="user")
    teachout = ndb.KeyProperty(required=True, kind="teachout")
    date = ndb.DateTimeProperty(auto_now_add=True)


class payments(ndb.Model):
    teachout = ndb.KeyProperty(required=True, kind="teachout")
    date = ndb.DateTimeProperty(auto_now_add=True)
    teacher = ndb.KeyProperty(kind="teacher")
    cantidad = ndb.FloatProperty(required=True)
    metodo = ndb.StringProperty()
    charge = ndb.StringProperty()


class msg(ndb.Model):
    mFrom = ndb.KeyProperty(kind="user")
    mTo = ndb.KeyProperty(kind="user")
    created = ndb.DateTimeProperty(auto_now_add=True)
    mensaje = ndb.TextProperty()


class chat(ndb.Model):
    msgs = ndb.StructuredProperty(msg, repeated=True)
    teacher = ndb.KeyProperty(kind="teacher")
    # user es el parent
