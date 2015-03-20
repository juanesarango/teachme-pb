from twilio.rest import TwilioRestClient
from google.appengine.api import urlfetch
from con import settings
import urllib
import json

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN


class IceServersHelper():

    @classmethod
    def make_ice_servers(cls):
        client = TwilioRestClient(account_sid, auth_token)
        token = client.tokens.create()
        # newIceServers = [
        #     {"uris": []}
        #     ]
        # for server in token.ice_servers:
        #     if "url" in server:
        #         newIceServers[0]['uris'].append(server["url"])
        #     if "credential" in server:
        #         newIceServers[0]['password'] = server["credential"]
        #     if "username" in server:
        #         newIceServers[0]['username'] = server["username"]
        cls.create_room_xir("1234")
        xirSysServers = cls.create_turn_servers("1234")
        for i in xirSysServers:
            token.ice_servers.append(i)

        return token.ice_servers

    @classmethod
    def create_room_xir(cls, room):
        tok = {'ident': 'teachme',
               'secret': settings.XIRSYS_AUTH_TOKEN,
               'domain': 'www.teachmeapp.com',
               'application': 'session',
               'room': 'default', }
        data = urllib.urlencode(tok)
        url = 'https://api.xirsys.com/addRoom'
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST)
        return response

    @classmethod
    def create_turn_servers(cls, room):
        tok = {'ident': 'teachme',
               'secret': settings.XIRSYS_AUTH_TOKEN,
               'domain': 'www.teachmeapp.com',
               'application': 'session',
               'room': 'default',
               'secure': 1}
        data = urllib.urlencode(tok)
        url = 'https://api.xirsys.com/getIceServers'
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST)
        serv = json.loads(response.content)
        return serv['d']['iceServers']
