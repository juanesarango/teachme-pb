from api.helpers import BaseApiHelper
from api.messages import TokenResponseMessage

from core.models import Token
from core.models import User

import datetime


class TokenApiHelper(BaseApiHelper):

    _model = Token

    def to_message(self, entity):
        return TokenResponseMessage(
            acces_token=entity.acces_token,
            token_type=entity.token_type)

    def grant_token(self, request):
        user = User.login(request.username, request.password)
        if not user:
            return None
        user_has_token = self.user_has_token(user)
        if user_has_token:
            return user_has_token
        else:
            new_token = self.create_new_token(user)
            return new_token

    def user_has_token(self, user):
        user_token = Token.query(Token.user == user.key.id()).get()
        if self.token_still_valid(user_token):
            return user_token
        else:
            return False

    def token_still_valid(self, token):
        now = datetime.now()
        token_expiration = token.created + datetime.timedelta(days=30)
        if token_expiration < now:
            token.key.delete()
            return False
        else:
            return True

    def create_new_token(self, user):
        new_token = Token(user=user.key)
        new_token.put()
        return new_token
