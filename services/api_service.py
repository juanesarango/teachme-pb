import endpoints
from api.controllers import TokenEndPoint
from api.controllers import UserEndpoint


APPLICATION = endpoints.api_server([
    TokenEndPoint,
    UserEndpoint
    ])
