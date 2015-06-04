import endpoints
from protorpc import messages
from protorpc import message_types

from teacher_api_messages import TeacherRequest
from teacher_api_messages import TeacherResponse
from teacher_api_messages import TeacherListResponse
from teacher_api_messages import ReviewResponse


Teacher_resource = endpoints.ResourceContainer(
    TeacherRequest,
    id=messages.IntegerField(1, variant=messages.Variant.INT64, required=True)
)

from user_api_messages import UserRequestMessage
from user_api_messages import UserResponseMessage
from user_api_messages import UserListResponseMessage

User_resource = endpoints.ResourceContainer(
    UserRequestMessage,
    id=messages.IntegerField(1, variant=messages.Variant.INT64, required=True)
    )

from token_api_messages import TokenRequestMessage
from token_api_messages import TokenResponseMessage
