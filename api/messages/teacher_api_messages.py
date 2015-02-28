from protorpc import messages
from protorpc import message_types
from api.messages import AreaResponse


class ReviewResponse(messages.Message):
    rating = messages.IntegerField(1)
    comment = messages.StringField(2)
    user = messages.StringField(3)
    teachout = messages.StringField(4)
    date = messages.StringField(5)


class TeacherResponse(messages.Message):
    id = messages.IntegerField(1)
    name = messages.StringField(2)
    lname = messages.StringField(3)
    mail = messages.StringField(4)
    about = messages.StringField(5)
    fee = messages.IntegerField(6)
    profilePic = messages.StringField(7)
    ciudad = messages.StringField(8)
    pais = messages.StringField(9)
    idiomas = messages.StringField(10, repeated=True)
    linkedin = messages.StringField(11)
    areas = messages.MessageField(AreaResponse, 12, repeated=True)
    timezoneOffset = messages.IntegerField(13)
    tags = messages.StringField(14, repeated=True)
    dateAvailable = message_types.DateTimeField(15, repeated=True)
    dateReserved = messages.IntegerField(16, repeated=True)
    teachouts = messages.IntegerField(17, repeated=True)
    teachoutsExpired = messages.IntegerField(18, repeated=True)
    rating = messages.FloatField(19)
    reviews = messages.MessageField(ReviewResponse, 20, repeated=True)
    score = messages.IntegerField(21)
    aceptado = messages.BooleanField(22)
    movil = messages.IntegerField(23)


class TeacherListResponse(messages.Message):
    teachers = messages.MessageField(TeacherResponse, 1, repeated=True)
    count = messages.IntegerField(2)


class TeacherRequest(messages.Message):
    name = messages.StringField(1)
    lname = messages.StringField(2)
    mail = messages.StringField(3)
    about = messages.StringField(4)
    fee = messages.IntegerField(5)
    profilePic = messages.StringField(6)
    ciudad = messages.StringField(7)
    pais = messages.StringField(8)
    idiomas = messages.StringField(9, repeated=True)
    linkedin = messages.StringField(10)
    areas = messages.IntegerField(11, repeated=True)
    timezoneOffset = messages.IntegerField(12)
    tags = messages.StringField(13, repeated=True)
    dateAvailable = messages.StringField(14, repeated=True)
    dateReserved = messages.IntegerField(15, repeated=True)
    teachouts = messages.IntegerField(16, repeated=True)
    teachoutsExpired = messages.IntegerField(17, repeated=True)
    rating = messages.FloatField(18)
    reviews = messages.StringField(19, repeated=True)
    score = messages.IntegerField(20)
    aceptado = messages.BooleanField(21)
    movil = messages.IntegerField(22)
