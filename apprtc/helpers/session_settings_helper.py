from core.helpers import FirebaseHelper


class SessionSettingsHelper():

    @classmethod
    def create_session_settings(cls, session_id=None):
        if session_id:
            url = 'https://teachmeapp.firebaseio.com/session'
            session_settings = {"whiteBoard": "false",
                                "userId1": 456,
                                "userId2": 678,
                                "userName1": "Julian",
                                "userName2": "Juanes",
                                "userOnline1": "true",
                                "userOnline2": "false"}
            result = FirebaseHelper.PUT(
                url, session_id, session_settings, {})
            return result
        else:
            return False
