import requests
import io, os

class Config:
    USER_ID: str = ''
    USER_AUTH_ID: str = ''
    CLIENT_ID: str = ''
    COMPLETE_STEP_URL: str = ''
    FAIL_STEP_URL: str = ''
    ATTACH_FILE_URL: str = ''

    def __init__(self, user_id: str, user_auth_id: str, client_id: str, complete_step_url: str, fail_step_url: str, attach_file_url: str):
        self.USER_ID = user_id
        self.USER_AUTH_ID = user_auth_id
        self.CLIENT_ID = client_id
        self.COMPLETE_STEP_URL = complete_step_url
        self.FAIL_STEP_URL = fail_step_url
        self.ATTACH_FILE_URL = attach_file_url

class Api:
    def __init__(self, config: Config, logging = None):
        self.__logging = logging
        self.__config = config
        self.__user_id = config.USER_ID
        self.__user_auth_id = config.USER_AUTH_ID
        self.__client_id = config.CLIENT_ID
        self.__coachbot_complete_step_url = config.COMPLETE_STEP_URL
        self.__coachbot_fail_step_url = config.FAIL_STEP_URL
        self.__coachbot_attach_file_url = config.ATTACH_FILE_URL

    def attach_file_to_step(self, playExecutionId: str, stepIdentifier: str, file_name: str, file_contents: bytes):
        file_like_object = io.BytesIO(file_contents)
        files = {'file': (file_name, file_like_object)}
        headers = { 
            **self.__build_headers(), 
            **{
                'playExecutionId': playExecutionId,
                'stepIdentifier': stepIdentifier
            }
        }
        requests.post(self.__coachbot_attach_file_url, headers=headers, files=files)

    def complete_step(self, playExecutionId: str, stepIdentifier: str, collectedData: dict = {}):
        data = {
            'playExecutionId': playExecutionId,
            'stepIdentifier': stepIdentifier,
            'collectedData': collectedData
        }
        requests.post(self.__coachbot_complete_step_url, json=data, headers=self.__build_headers())

    def fail_step(self, playExecutionId: str, stepIdentifier: str):
        data = {
            'playExecutionId': playExecutionId,
            'stepIdentifier': stepIdentifier
        }
        requests.post(self.__coachbot_fail_step_url, json=data, headers=self.__build_headers())

    def __build_headers(self):
        return {
            'userId': self.__user_id,
            'authId': self.__user_auth_id,
            'clientId': self.__client_id
        }
