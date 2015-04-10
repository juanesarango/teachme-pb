from core.helpers import FirebaseHelper


class SessionSettingsHelper():

    @classmethod
    def create_session_settings(cls, session_id=None, user1=None, user2=None):
        if session_id:
            if not cls.session_exist(session_id):
                url = 'https://teachmeapp.firebaseio.com/session'
                if user1 and user2:
                    session_settings = {"userId1": user1.key.id(),
                                        "userId2": user2.key.id(),
                                        "userName1": user1.name,
                                        "userName2": user2.name,
                                        "userOnline1": "false",
                                        "userOnline2": "false",
                                        "whiteBoard": "false"}
                else:
                    session_settings = {"userId1": "None",
                                        "userId2": "None",
                                        "userName1": "Guest",
                                        "userName2": "Guest",
                                        "userOnline1": "false",
                                        "userOnline2": "false",
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
