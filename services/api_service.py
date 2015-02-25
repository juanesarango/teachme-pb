import endpoints
from api.controllers import TeacherEndpoint


APPLICATION = endpoints.api_server([
    TeacherEndpoint
    ])
