from core.models import BaseModel
from google.appengine.ext import ndb
import random
import hashlib
from string import letters


class User(BaseModel):
    # Essentials
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    passwordHash = ndb.StringProperty()
    timeZoneOffset = ndb.IntegerProperty()
    role = ndb.StringProperty()

    lastName = ndb.StringProperty()
    # Facebook
    picture = ndb.StringProperty()
    gender = ndb.StringProperty()

    # Optionals
    mobilePhoneNumber = ndb.IntegerProperty()
    expert = ndb.IntegerProperty()

    verificated = ndb.BooleanProperty()

    sessions = ndb.IntegerProperty(repeated=True)

    transactions = ndb.IntegerProperty(repeated=True)

    @classmethod
    def signup(cls, request):
        passwordHashed = cls.make_password_hash(request.email,
                                                request.passwordString)
        new_user = User(name=request.name,
                        email=request.email,
                        passwordHash=passwordHashed,
                        timeZoneOffset=request.timeZoneOffset)
        new_user.put()
        return new_user

    @classmethod
    def login(cls, email, passwordString):
        user = cls.get_by_email(email)
        if user and cls.validate_password(email,
                                          passwordString,
                                          user.passwordHash):
            return user
        else:
            return None

    @classmethod
    def get_by_email(cls, email=None):
        if email:
            return cls.query(cls.email == email).get()
        else:
            return None

    @classmethod
    def make_salt(cls, length=7):
        return ''.join(random.choice(letters) for x in xrange(length))

    @classmethod
    def make_password_hash(cls, name, passwordString, salt=None):
        if not salt:
            salt = cls.make_salt()
        hashString = hashlib.sha256(name + passwordString + salt).hexdigest()
        return '%s,%s' % (salt, hashString)

    @classmethod
    def validate_password(cls, name, password, passwordHash):
        salt = passwordHash.split(',')[0]
        return passwordHash == cls.make_password_hash(name, password, salt)
