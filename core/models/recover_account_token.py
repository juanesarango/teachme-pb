from core.models import BaseModel
from google.appengine.ext import ndb


class RecoverAccountToken(BaseModel):
    user = ndb.KeyProperty(required=True)
    recovered = ndb.BooleanProperty()

    @classmethod
    def create(cls, user, recovered=False):
        token = RecoverAccountToken(user=user, recovered=recovered)
        token.put()
        return token.key.urlsafe()
