# -*- coding: utf-8 -*-
import csv
from teachme_db import user as User
from teachme_db import teacher as Teacher


class DownloadDB():

    @classmethod
    def all_mails(cls):
        cls.user_mails()
        cls.mentor_mails()

    @classmethod
    def user_mails(cls):
        users = User.query().fetch()
        users_file = open('users_db.csv', 'wt')
        try:
            writer = csv.writer(users_file)
            for user in users:
                writer.writerow((user.name.encode('utf-8'), user.lname.encode('utf-8'), user.mail.encode('utf-8')))
        finally:
            users_file.close()
            print "You got users mails"

    @classmethod
    def mentor_mails(cls):
        teachers = Teacher.query().fetch()
        teachers_file = open('teachers_db.csv', 'wt')
        try:
            writer = csv.writer(teachers_file)
            for teacher in teachers:
                writer.writerow((teacher.name.encode('utf-8'), teacher.lname.encode('utf-8'), teacher.mail.encode('utf-8')))
        finally:
            teachers_file.close()
            print "You got mentors mails"
