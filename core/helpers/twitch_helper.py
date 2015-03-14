from core.helpers import BaseHelper
from google.appengine.api import urlfetch
import json


class TwitchHelper(BaseHelper):

    @classmethod
    def is_channel_live(cls, channel):
        '''
        curl -H 'Accept: application/vnd.twitchtv.v3+json' -X GET https://api.twitch.tv/kraken/streams/test_channel
        '''
        if channel:
            url = "https://api.twitch.tv/kraken/streams/{}".format(channel)
            headers = {'Accept': 'application/vnd.twitchtv.v3+json'}
            response = urlfetch.fetch(
                url=url,
                method=urlfetch.GET,
                headers=headers)
            if response.status_code == 200:
                response_dict = json.loads(response.content)
                if response_dict['stream']:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
