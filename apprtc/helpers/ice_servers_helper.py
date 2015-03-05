from twilio.rest import TwilioRestClient
import requests
import json

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC72f22161a9c99728f48fe1584fe9f59b"
auth_token = "6b7c664f6d0a5d9191bfb2d7d7e47f05"


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

#   Make room in xirsys
    @classmethod
    def create_room_xir(cls, room):
        tok = {'ident': 'teachme',
               'secret': '82643c69-1891-41ec-aade-a24a484f9689',
               'domain': 'www.teachmeapp.com',
               'application': 'session',
               'room': room, }
        url = 'https://api.xirsys.com/addRoom'
        requests.post(url, data=tok)
        return

#   Turn as a service xirsys
    @classmethod
    def create_turn_servers(cls, room):
        tok = {'ident': 'teachme',
               'secret': '82643c69-1891-41ec-aade-a24a484f9689',
               'domain': 'www.teachmeapp.com',
               'application': 'session',
               'room': room,
               'secure': 1}
        url = 'https://api.xirsys.com/getIceServers'
        r = requests.post(url, data=tok)
        serv = json.loads(r.content)
        return serv['d']['iceServers']
