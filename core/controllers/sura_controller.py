import json
import booking
import fns

from core.controllers import BaseController
from core.helpers import MentorHelper

from teachme_db import areas as Area
from teachme_db import teacher as Teacher
from teachme_db import tags as Tag
from teachme_db import review as Review

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import logging

class SuraController(BaseController):

  def get(self, ar=None):
    if not self.user:
      self.redirect('/login?redirect=/sura')
      return
    if self.company != 'sura':
      self.abort(403)
    if ar:
      area = Area.query(Area.url == ar).get()
      if not area:
        area = Area.get_by_id(int(ar))
    else:
      area = Area.query().get()
    if area:
      mentors = Teacher.query(ndb.AND(Teacher.areas == area.key.id(), Teacher.aceptado == True)).fetch()
      MentorHelper.sort_mentors(mentors)
      self.render("sura_main.html", mentors=mentors, area=area)
      return
    self.abort(500)


class SuraProfileController(blobstore_handlers.BlobstoreUploadHandler, BaseController):
  
  def get(self, te_id):
    logging.error('Company', self.company)
    if not self.user:
      self.redirect('/login?redirect=/sura')
      return
    if self.company != 'sura':
      self.abort(403)
    teacher = ndb.Key(Teacher, int(te_id), parent=self.user.key).get()
    if not teacher:
      self.abort(403)
      return
    reviews = Review.query(ancestor=teacher.key).order(-Review.date)
    fechas = json.dumps(booking.UTCfechas(teacher.date_available))
    dates = json.dumps(fns.solo_dates(teacher.date_available))
    hours = json.dumps(fns.solo_hours(teacher.date_available))
    upload_url = blobstore.create_upload_url('/upload')
    taglist = json.dumps(Tag.query().get().name) if Tag.query().get() else []
    self.render("profile_teacher.html", teacher=teacher, upload_url=upload_url, dates=dates, hours=hours, fechas=fechas, taglist=taglist, reviews=reviews)

  def post(self):
    te_id = self.request.get("te_id")
    teacher = ndb.Key(Teacher, int(te_id), parent=self.user.key).get()
    profile_pic = self.get_uploads("profile_pic")
    if profile_pic:
      blob_info = profile_pic[0]
      if teacher.profile_pic:
        if teacher.profile_pic_r:
          images.delete_serving_url(teacher.profile_pic)
        blobstore.delete(teacher.profile_pic)
      teacher.profile_pic = blob_info.key()
      teacher.profile_pic_r = images.get_serving_url(teacher.profile_pic, size=200, secure_url=True)
      self.user.profile_pic = blob_info.key()
      self.user.profile_pic_r = teacher.profile_pic_r
      teacher.put()
      self.user.put()
    self.redirect("/profile/teacher/%s" % str(teacher.key.id()))
