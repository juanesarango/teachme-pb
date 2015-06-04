import endpoints
from protorpc import message_types

from api import teachme_api
from api.controllers import BaseApiController
from api.helpers import UserApiHelper
from api.messages import UserRequestMessage
from api.messages import UserResponseMessage
from api.messages import UserListResponseMessage

from core.models import User


@teachme_api.api_class(resource_name='user', path='users')
class UserEndpoint(BaseApiController):

    # If normal user, get his account. Admin, get all
    # @endpoints.method(messages_types.VoidMessage,
    #                   UserListResponseMessage,
    #                   path='/users',
    #                   http_method='GET',
    #                   name='get_all')
    # def get_users(self, request):

    @endpoints.method(UserRequestMessage,
                      UserListResponseMessage,
                      path='/users',
                      http_method='POST',
                      name='create_user')
    def create_user(self, request):
        if not (request.name and request.email and request.passwordString):
            raise endpoints.BadRequestException(
                'name, email and password are mandatory')
        new_user = User.signup(request)
        return UserListResponseMessage(
            users=[UserApiHelper().to_message(new_user)])
