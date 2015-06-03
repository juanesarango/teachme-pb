from protorpc import messages
from protorpc import message_types


class TokenResponseMessage(messages.Message):
    acces_token = messages.StringField(1)
    token_type = messages.StringField(2)


class TokenRequestMessage(message_types.VoidMessage):
    pass
