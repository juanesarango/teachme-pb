from core.models import BaseModel
from google.appengine.ext import ndb


class Token(BaseModel):
    user = ndb.IntegerProperty()
    role = ndb.StringProperty()
