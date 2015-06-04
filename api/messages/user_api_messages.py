from protorpc import messages
from protorpc import message_types


class UserRequestMessage(messages.Message):
    name = messages.StringField(1)
    lastName = messages.StringField(2)
    email = messages.StringField(3)
    passwordString = messages.StringField(4)
    passwordStringConfirmation = messages.StringField(5)
    picture = messages.StringField(6)
    mobilePhoneNumber = messages.StringField(7)
    expert = messages.StringField(8)
    verificated = messages.BooleanField(9)
    sessions = messages.IntegerField(10, repeated=True)
    transactions = messages.IntegerField(11, repeated=True)
    timeZoneOffset = messages.IntegerField(12)


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
