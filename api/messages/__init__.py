import endpoints
from protorpc import messages
from protorpc import message_types

from area_api_message import AreaResponse
from teacher_api_messages import TeacherRequest
from teacher_api_messages import TeacherResponse
from teacher_api_messages import TeacherListResponse
from teacher_api_messages import ReviewResponse


Teacher_resource = endpoints.ResourceContainer(
    TeacherRequest,
    id=messages.IntegerField(1, variant=messages.Variant.INT64, required=True)
)
