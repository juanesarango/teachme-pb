import endpoints
from protorpc import message_types

from api import teachme_api
from api.controllers import BaseApiController

from api.messages import TokenRequestMessage
from api.messages import TokenResponseMessage

from api.helpers import TokenApiHelper


@teachme_api.api_class(resource_name='token', path='token')
class TokenEndPoint(BaseApiController):

    @endpoints.method(TokenRequestMessage,
                      TokenResponseMessage,
                      path='/token',
                      http_method='POST',
                      name='create')
    def create_token(self, request):
        if not (request.username and request.password):
            raise endpoints.BadRequestException(
                "The client doesn't provide the username and password")
        token = TokenApiHelper().grant_token(request)
        if not token:
            raise endpoints.BadRequestException(
                'email and password incorrect')
        return TokenApiHelper().to_message(token)
