import requests
import io, os

class CoachbotApi:
    def __init__(self, logging, user_id: str, user_auth_id: str, client_id: str):
        self.__logging = logging
        self.__user_id__ = user_id
        self.__user_auth_id__ = user_auth_id
        self.__client_id__ = client_id
        self.__coachbot_attach_file_url__ = os.getenv('COACHBOT_ATTACH_FILE_ENDPOINT')
        self.__coachbot_complete_step_url__ = os.getenv('COACHBOT_COMPLETE_STEP_ENDPOINT')
        self.__coachbot_fail_step_url__ = os.getenv('COACHBOT_FAIL_STEP_ENDPOINT')

    def attach_file_to_step(self, playExecutionId: str, stepIdentifier: str, file_name: str, file_contents: bytes):
        file_like_object = io.BytesIO(file_contents)
        files = {'file': (file_name, file_like_object)}
        headers = { 
            **self.__build_headers__(), 
            **{
                'playExecutionId': playExecutionId,
                'stepIdentifier': stepIdentifier
            }
        }
        requests.post(self.__coachbot_attach_file_url__, headers=headers, files=files)

    def complete_step(self, playExecutionId: str, stepIdentifier: str, collectedData: dict = {}):
        data = {
            'playExecutionId': playExecutionId,
            'stepIdentifier': stepIdentifier,
            'collectedData': collectedData
        }
        requests.post(self.__coachbot_complete_step_url__, json=data, headers=self.__build_headers__())

    def fail_step(self, playExecutionId: str, stepIdentifier: str):
        data = {
            'playExecutionId': playExecutionId,
            'stepIdentifier': stepIdentifier
        }
        requests.post(self.__coachbot_fail_step_url__, json=data, headers=self.__build_headers__())

    def __build_headers__(self):
        return {
            'userId': self.__user_id__,
            'authId': self.__user_auth_id__,
            'clientId': self.__client_id__
        }
