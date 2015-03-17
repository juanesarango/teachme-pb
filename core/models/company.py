from core.models import BaseModel
from google.appengine.ext import ndb


class Company(BaseModel):
    name = ndb.StringProperty()
    domain = ndb.StringProperty()
    urldomain = ndb.StringProperty()
    areas = ndb.KeyProperty(repeated=True)
    logo = ndb.StringProperty()
    email_domain = ndb.StringProperty()
