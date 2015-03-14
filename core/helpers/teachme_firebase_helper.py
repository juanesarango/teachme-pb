import urllib2
import urlparse
from google.appengine.api import urlfetch
# from firebase_token_generator import FirebaseTokenGenerator
import json
from core.helpers import BaseHelper

class FirebaseHelper(BaseHelper):

    NAME_EXTENSION = '.json'
    URL_SEPERATOR = '/'

    # def __init__(self, dsn, authentication=None):
    #     assert dsn.startswith('https://'), 'DSN must be a secure URL'
    #     self.dsn = dsn
    #     self.authentication = authentication
    @classmethod
    def _build_endpoint_url(self, url, name=None):
        """
        Method that constructs a full url with the given url and the
        snapshot name.
        Example:
        full_url = _build_endpoint_url('/users', '1')
        full_url => 'http://firebase.localhost/users/1.json'
        """
        if not url.endswith(self.URL_SEPERATOR):
            url = url + self.URL_SEPERATOR
        if name is None:
            name = ''
        return '%s%s%s' % (url, name,
                           self.NAME_EXTENSION)

    @classmethod
    def PUT(cls, url, name, data, auth):
        """ 
        Write or replace data to a defined path, like messages/users/user1/<data>
        """
        endpoint = cls._build_endpoint_url(url, name)
        data = json.dumps(data)
        response = urlfetch.fetch(
            url=endpoint,
            payload=data,
            method=urlfetch.PUT)
        return response

    @classmethod
    def POST(cls, url, name, data, auth):
        """ 
        Add to a list of data in Firebase. Every time you send a POST
        request Firebase generates a unique ID, like
        messages/users/<unique-id>/<data>
        """
        endpoint = cls._build_endpoint_url(url, name)
        data = json.dumps(data)
        response = urlfetch.fetch(
            url=endpoint,
            payload=data,
            method=urlfetch.POST)
        return response

    @classmethod
    def PATCH(cls, url, name, data, auth):
        """ 
        Update some of the keys for a defined path without replacing all of the data.
        """
        endpoint = cls._build_endpoint_url(url, name)
        data = json.dumps(data)
        response = urlfetch.fetch(
            url=endpoint,
            payload=data,
            method=urlfetch.PATCH)
        return response

    @classmethod
    def DELETE(cls, url, name, auth):
        """ 
        Remove data from the specified Firebase reference.
        """
        endpoint = cls._build_endpoint_url(url, name)
        response = urlfetch.fetch(
            url=endpoint,
            method=urlfetch.DELETE
            )
        return response
