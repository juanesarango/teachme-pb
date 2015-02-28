import endpoints
from google.appengine.ext import ndb

from protorpc import message_types

from api import teachme_api
from api.controllers import BaseApiController
from api.helpers import TeacherApiHelper
from api.messages import TeacherListResponse
from api.messages import Teacher_resource
from api.messages import TeacherRequest

from teachme_db import teacher as Teacher
from core.helpers import MentorHelper


@teachme_api.api_class(resource_name='teacher', path='teachers')
class TeacherEndpoint(BaseApiController):

    @endpoints.method(message_types.VoidMessage, TeacherListResponse,
                      path='/teachers', http_method='GET',
                      name='get_all')
    def get_teachers(self, request):
        teachers = Teacher.query().fetch()
        return TeacherListResponse(
          teachers=[TeacherApiHelper().to_message(teacher) for teacher in teachers if teachers])

    @endpoints.method(Teacher_resource, TeacherListResponse,
                      path='{id}', http_method='GET',
                      name='get_one')
    def get_teacher(self, request):
        teacher = Teacher.get_by_id(request.id, parent=ndb.Key('user', 5629499534213120))
        if not teacher:
            raise endpoints.NotFoundException(
              "The teacher ID: " + str(request.id) + " doesn't exist")
        return TeacherListResponse(teachers=[TeacherApiHelper().to_message(teacher)])

    @endpoints.method(TeacherRequest, TeacherListResponse,
                      path='/teachers', http_method='POST',
                      name='create')
    def create_teacher(self, request):
        if not request.name and not request.lname:
            raise endpoints.BadRequestException('The data: name and last name are obligatory.')
        teacher = MentorHelper.create(request)
        if not teacher:
            raise endpoints.BadRequestException('It was not possible to create the teacher')
        return TeacherListResponse(teachers=[TeacherApiHelper().to_message(Teacher.get())])

    @endpoints.method(Teacher_resource, TeacherListResponse,
                      path='{id}', http_method='PUT',
                      name='update')
    def update_teacher(self, request):
        teacher = Teacher.get_by_id(request.id)
        if not teacher:
            raise endpoints.NotFoundException(
              "The teacher ID: " + str(request.id) + " doesn't exist")
        if not request.name and not request.lname:
            raise endpoints.BadRequestException('The data: title, country are obligatory.')
        teacher = MentorHelper.update(teacher.key, request)
        if not teacher:
            raise endpoints.BadRequestException('It was not possible to create the teacher')
        return TeacherListResponse(teachers=[TeacherApiHelper().to_message(Teacher.get())])

    @endpoints.method(Teacher_resource, message_types.VoidMessage,
                      path='{id}', http_method='DELETE',
                      name='delete')
    def delete_teacher(self, request):
        teacher = Teacher.get_by_id(request.id)
        if not teacher:
            raise endpoints.NotFoundException(
              "The teacher ID: " + str(request.id) + " doesn't exist")
        Teacher.key.delete()
        return message_types.VoidMessage()
