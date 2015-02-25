from google.appengine.api import mail


class BaseHelper(object):

    @classmethod
    def send_email(cls, to_user, subject, body):
        sender = "Teachme team <info@teachmeapp.com>"
        to = to_user.name + " " + to_user.lname + "<" + to_user.mail + ">"
        mail.send_mail(sender=sender, to=to, subject=subject, body=body)
