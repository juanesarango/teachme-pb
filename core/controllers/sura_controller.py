from core.controllers import BaseController
from core.helpers import MentorHelper

from teachme_db import areas, teacher

from google.appengine.ext import ndb


class SuraController(BaseController):

    def get(self, ar=None):
        if ar:
            area = areas.query(areas.url == ar).get()
            if not area:
                area = areas.get_by_id(int(ar))
        else:
            area = areas.query().get()
        if area:
            mentors = teacher.query(ndb.AND(teacher.areas == area.key.id(), teacher.aceptado == True)).fetch()
            MentorHelper.sort_mentors(mentors)
            self.render("sura_main.html", mentors=mentors, area=area)
            return
        self.abort(500)
