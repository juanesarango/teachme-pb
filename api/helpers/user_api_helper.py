from api.helpers import BaseApiHelper
from api.messages import UserResponseMessage

from core.models import User


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
