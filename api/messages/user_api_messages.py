from protorpc import messages
from protorpc import messages_types


class UserRequestMessage(messages.Message):
    name = messages.StringField(1)
    lastName = messages.StringField(2)
    email = messages.StringField(3)
    picture = messages.StringField(4)
    mobilePhoneNumber = messages.StringField(5)
    expert = messages.StringField(6)
    verificated = messages.BooleanField(7)
    sessions = messages.IntegerField(8, repeated=True)
    transactions = messages.IntegerField(9, repeated=True)


class UserResponseMessage(messages.Message):
    id = messages.IntegerField(1)
    name = messages.StringField(2)
    lastName = messages.StringField(3)
    email = messages.StringField(4)
    picture = messages.StringField(5)
    mobilePhoneNumber = messages.StringField(6)
    expert = messages.StringField(7)
    verificated = messages.BooleanField(8)
    sessions = messages.IntegerField(9, repeated=True)
    transactions = messages.IntegerField(10, repeated=True)


class UserListResponseMessage(messages.Message):
    users = messages.MessageField(UserResponseMessage, 1, repeated=True)
