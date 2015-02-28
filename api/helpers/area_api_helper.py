from api.helpers import BaseApiHelper
from api.messages import AreaResponse

from teachme_db import areas as Area


class AreaApiHelper(BaseApiHelper):

    _model = Area

    def to_message(self, teacher_areas, each_area):
        area = each_area
        return AreaResponse(
            id=area.key.id(),
            name=area.name,
            namet=area.namet,
            url=area.url,
            checked=True if area.key.id() in teacher_areas else False
            )
