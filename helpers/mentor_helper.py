from core.helpers import BaseHelper

import datetime


class MentorHelper(BaseHelper):

    @classmethod
    def sort_mentors(cls, mentors):

        def score_rating(rating, n):
            score = rating*w['rating']/n
            return score

        def score_reviews(reviews, n):
            reviews = n if reviews > n else reviews
            score = reviews*w['reviews']/n
            return score

        def score_hours(hours, n):
            now = datetime.datetime.now()
            count = 0
            for hour in hours:
                count += 1 if hour > now else 0
            hours = n if hours > n else hours
            score = hours*w['hours']/n
            return score

        def score_sessions(sessions, n):
            number_sessions = len(sessions)
            score = number_sessions*w['sessions']/n
            return score

        def score_pic(pic, n):
            score = w['pic']
            return score

        def score_about(about, n):
            number_char = len(about)
            if number_char > 200:
                value = n
            elif number_char > 100:
                value = n/2
            else:
                value = 0
            score = value*w['about']/n
            return score

        # Ponderate weigths %
        w = {'rating': 20,
             'reviews': 20,
             'hours': 20,
             'sessions': 20,
             'pic': 10,
             'about': 10
             }

        for m in mentors:
            rating = m.rating
            reviews = m.reviews
            hours = m.date_available
            sessions = m.teachouts_expired
            pic = m.profile_pic
            about = m.about

            score = 0
            score += score_rating(rating, 4) if rating else 0
            score += score_reviews(reviews, 4) if reviews else 0
            score += score_hours(hours, 4) if hours else 0
            score += score_sessions(sessions, 4) if sessions else 0
            score += score_pic(pic, 4) if pic else 0
            score += score_about(about, 4) if about else 0
            m.score = score

        return mentors.sort(key=lambda m: m.count)
