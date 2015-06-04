import endpoints
from api.controllers import TokenEndPoint


APPLICATION = endpoints.api_server([
    TokenEndPoint
    ])
