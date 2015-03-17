from core.models import BaseModel
from google.appengine.ext import ndb


class AreaCategory(BaseModel):
  name = ndb.StringProperty()
  company = ndb.KeyProperty()