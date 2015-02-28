from protorpc import messages


class AreaResponse(messages.Message):
    id = messages.IntegerField(1)
    name = messages.StringField(2)
    namet = messages.StringField(3)
    url = messages.StringField(4)
    checked = messages.BooleanField(5)
