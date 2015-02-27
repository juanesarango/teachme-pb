from api.helpers import BaseApiHelper
from api.messages import TeacherResponse
from api.messages import ReviewResponse

from teachme_db import teacher as Teacher
from teachme_db import review as Review


class TeacherApiHelper(BaseApiHelper):

    _model = Teacher

    def to_message(self, entity):
        return TeacherResponse(
            id=entity.key.id(),
            name=entity.name,
            lname=entity.lname,
            mail=entity.mail,
            about=entity.about,
            fee=entity.fee,
            profilePic=entity.profile_pic_r,
            ciudad=entity.ciudad,
            pais=entity.pais,
            idiomas=entity.idiomas,
            linkedin=entity.linkedin,
            areas=entity.areas,
            subareas=entity.subareas,
            timezoneOffset=entity.timezoneOffset,
            tags=entity.tags,
            dateAvailable=entity.date_available,
            dateReserved=entity.date_reserved,
            teachouts=entity.teachouts,
            teachoutsExpired=entity.teachouts_expired,
            rating=entity.rating,
            reviews=ReviewApiHelper().get_reviews(entity.key),
            score=entity.score,
            aceptado=entity.aceptado,
            movil=entity.movil,
            )


class ReviewApiHelper(BaseApiHelper):

    _model = Review

    def get_reviews(self, teacher_key):
        reviews = Review.query(ancestor=teacher_key).order(-Review.date)
        return [self.to_message(review) for review in reviews if reviews]

    def to_message(self, entity):
        return ReviewResponse(
            rating=entity.rating,
            comment=entity.comment,
            user=entity.user.get().name,
            # teachout=entity.teachout,
            # date=entity.date,
            )
