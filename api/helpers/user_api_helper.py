from api.helpers import BaseApiHelper
from api.messages import UserResponseMessage

from core.models import User

import re


class UserApiHelper(BaseApiHelper):

    _model = User

    def to_message(self, entity):
        return UserResponseMessage(
            id=entity.key.id(),
            name=entity.name,
            lastName=entity.lastName,
            email=entity.email,
            picture=entity.picture,
            mobilePhoneNumber=entity.mobilePhoneNumber,
            expert=entity.expert,
            verificated=entity.verificated,
            sessions=entity.sessions,
            transactions=entity.transactions)

    # Create user validations
    def valid_register(self, request):
        if not self.valid_string(request.name):
            return False
        if not self.valid_password(request.passwordString):
            return False
        elif request.passwordString != request.passwordStringConfirmation:
            return False
        if not self.valid_email(request.email):
            return False

        return True

    def valid_string(self, string):
        STRING_RE = re.compile(r"^.{3,20}$")
        return string and STRING_RE.match(string)

    def valid_password(self, password):
        PW_RE = re.compile(r"^.{6,20}")
        return password and PW_RE.match(password)

    def valid_email(self, email):
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        return not email or EMAIL_RE.match(email)
