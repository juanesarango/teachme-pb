from core.models import BaseModel
from google.appengine.ext import ndb


class Token(BaseModel):
    acces_token = ndb.ComputedProperty(lambda self: self.key.urlsafe())
    token_type = ndb.StringProperty(default='bearer')
    user = ndb.KeyProperty(required=True)
    role = ndb.StringProperty()
