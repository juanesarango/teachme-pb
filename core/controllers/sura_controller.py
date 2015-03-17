import time
import json
import booking
import fns
import webapp2

from core.controllers import BaseController
from core.helpers import MentorHelper

from teachme_db import areas as Area
from teachme_db import teacher as Teacher
from teachme_db import tags as Tag
from teachme_db import review as Review
from core.models import AreaCategory

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import logging


class SuraBaseController(BaseController):
  def initialize(self, *a, **kw):
    BaseController.initialize(self, *a, **kw)
    if not self.user:
      self.redirect('/login?redirect=/sura')
    if self.company.url_domain != 'sura':
      # Escribir No tiene autorizacion para entrar
      self.abort(403)


class SuraController(SuraBaseController):
  def get(self, ar=None):
    company_areas = Area.query(Area.company == self.company.key).order(Area.name).fetch()
    categories = AreaCategory.query(AreaCategory.company == self.company.key).fetch()
    if ar:
      area = Area.query(Area.url == ar).get()
      if not area:
        area = Area.get_by_id(int(ar))
    else:
      area = Area.query().get()
    if area:
      mentors = Teacher.query(ndb.AND(Teacher.areas == area.key.id(), Teacher.aceptado == True)).fetch()
      MentorHelper.sort_mentors(mentors)
      self.render("sura_main.html", mentors=mentors, area=area, company_areas=company_areas, categories=categories)
      return
    self.abort(500)


class SuraProfileController(blobstore_handlers.BlobstoreUploadHandler, SuraBaseController):
  def get(self, te_id):
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


class SuraAdminController(SuraBaseController):
  def initialize(self, *a, **kw):
    BaseController.initialize(self, *a, **kw)
    if self.user.mail not in self.company.admins:
       self.abort(403)

  def get(self):
    company_areas = Area.query(Area.company == self.company.key).order(Area.name).fetch()
    if not company_areas:
      company_areas = []
    categories = AreaCategory.query(AreaCategory.company == self.company.key).fetch()
    self.render("company_admin.html", company_areas=company_areas, categories=categories)
    return

  def post(self):
    area_name = self.request.get("area_name")
    area_category = self.request.get("area_category")
    area_key = self.request.get("area_key")
    if area_name and area_category:
      area_category = ndb.Key(urlsafe=area_category)
      new_area = Area(name=area_name, category=area_category, company=self.company.key)
      new_area.put()
      time.sleep(1)
    elif area_key:
      area = ndb.Key(urlsafe=area_key)
      area.delete()
      time.sleep(1)
    self.get()

