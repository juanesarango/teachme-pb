from helpers.mentor_helper import MentorHelper
from teachme_db import teacher
mentors = teacher.query().fetch()
MentorHelper.sort_mentors(mentors)
