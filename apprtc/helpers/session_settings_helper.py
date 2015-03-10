from firebase import firebase

firebase = firebase.FirebaseApplication('https://teachmeapp.firebaseio.com')


class SessionSettingsHelper():

    @classmethod
    def create_session(session_id=None):
        if session_id:
            session_settings = {"whiteboard": "false"}
            result = firebase.put(
                '/session', session_id, session_settings)
            return result
        else:
            return False
