from core.models import BaseModel
from google.appengine.ext import ndb


class Company(BaseModel):
    name = ndb.StringProperty()
    email_domain = ndb.StringProperty()
    url_domain = ndb.StringProperty()
    areas = ndb.KeyProperty(repeated=True)
    logo = ndb.StringProperty()
    admins = ndb.StringProperty(repeated=True)
