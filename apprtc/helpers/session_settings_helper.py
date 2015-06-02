from core.helpers import FirebaseHelper


class SessionSettingsHelper():

    @classmethod
    def create_session_settings(cls, session_id=None, user1=None, user2=None):
        if session_id:
            if not cls.session_exist(session_id):
                url = 'https://teachmeapp.firebaseio.com/session'
                if user1 and user2:
                    session_settings = {"participants": [user1.key.id(), user2.key.id()],
                                        "whiteBoard": "false"}
                else:
                    session_settings = {"participants": [],
                                        "whiteBoard": "false"}
                result = FirebaseHelper.PUT(
                    url, session_id, session_settings)
                return result
            else:
                return
        else:
            return False

    @classmethod
    def session_exist(cls, session_id=None):
        if session_id:
            url = "https://teachmeapp.firebaseio.com/session"
            result = FirebaseHelper.GET(url, session_id)
            if result.status_code == 200 and result.content != 'null':
                return True
            else:
                return False
            return result
        else:
            return False
