from protorpc import messages
from protorpc import messages_types


class UserResponseType(messages.Message):
    name = messages.StringField(1)
    lastName = messages.StringField(2)
    email = messages.StringField(3)
    picture = messages.StringField(4)
    mobilePhoneNumber = messages.StringField(5)
    expert = messages.StringField(6)
    verificated = messages.BooleanField(7)
    sessions = messages.IntegerField(8, repeated=True)
    transactions = messages.IntegerField(9, repeated=True)
