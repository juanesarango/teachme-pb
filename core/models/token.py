from core.models import BaseModel
from google.appengine.ext import ndb


class Token(BaseModel):
    token_type = ndb.StringProperty(default='bearer')
    user = ndb.KeyProperty(required=True)
    role = ndb.StringProperty()
