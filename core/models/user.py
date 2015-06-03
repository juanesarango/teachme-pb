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
    def signUp(cls, name, email, passwordString, timeZoneOffset):
        passwordHash = cls.makePasswordHash(email, passwordString)
        return User(name=name,
                    email=email,
                    passwordHash=passwordHash,
                    timeZoneOffset=timeZoneOffset)

    @classmethod
    def login(cls, email, passwordString):
        user = cls.getByEmail(email)
        if user and cls.validatePassword(email,
                                         passwordString,
                                         user.passwordHash):
            return user
        else:
            return None

    @classmethod
    def getByEmail(cls, email=None):
        if email:
            return cls.query(cls.email == email).get()
        else:
            return None

    @classmethod
    def makeSalt(cls, length=7):
        return ''.join(random.choice(letters) for x in xrange(length))

    @classmethod
    def makePasswordHash(cls, name, passwordString, salt=None):
        if not salt:
            salt = cls.makeSalt()
        hashString = hashlib.sha256(name + passwordString + salt).hexdigest()
        return '%s,%s' % (salt, hashString)

    @classmethod
    def validatePassword(cls, name, password, passwordHash):
        salt = passwordHash.split(',')[0]
        return passwordHash == cls.makePasswordHash(name, password, salt)
