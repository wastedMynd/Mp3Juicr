import os
import base64
import requests
import datetime


# region getters for: client_id, client_secret, client_credentials, client_credentials_encoded, etc..
def get_client_id() -> str:
    return os.environ.get('SPOTIFY_CLIENT_ID')


def get_client_secret() -> str:
    return os.environ.get('SPOTIFY_CLIENT_SECRET')


def get_client_credentials() -> str:
    return f'{get_client_id()}:{get_client_secret()}'


def get_client_credentials_encoded() -> bytes:
    return get_client_credentials().encode()


def get_client_credentials_encoded_as_base64() -> base64:
    return base64.b64encode(get_client_credentials_encoded())


def get_client_credentials_decode():
    return get_client_credentials_encoded_as_base64().decode()


def get_client_token_url() -> str:
    return os.environ.get('SPOTIFY_CLIENT_TOKEN_URL')


def get_client_token_data() -> dict:
    return {'grant_type': 'client_credentials'}


def get_client_token_header() -> dict:
    return {'Authorization': f'Basic {get_client_credentials_decode()}'}


# endregion


def check_if_response_is_good(response):
    return response.ok and response.status_code in range(200, 300)


def get_auth_response():
    with requests.post(url=get_client_token_url(), headers=get_client_token_header(), data=get_client_token_data()) as response:
        if not check_if_response_is_good(response):
            return None
    return response


def get_time_now():
    return datetime.datetime.now()


def get_time_delta_of(seconds_in_time):
    return datetime.timedelta(seconds=seconds_in_time)


def get_future_time_of(when, then):
    return when + get_time_delta_of(then)


class SpotifyAuthenticateClient(object):
    def __init__(self):
        self.__access_token = None
        self.__token_type = None
        self.__expires_in = None
        self.__scope = None
        self.__time_of_access_token_request = 0
        self.__did_authenticate = False
        self.perform_authentication()
        pass

    def perform_authentication(self):
        self.__time_of_access_token_request = get_time_now()

        self.__did_authenticate = (response := get_auth_response()) is not None

        if self.did_authenticate():
            self.__setup_attributes(response)

        pass

    def __setup_attributes(self, response):
        response_json_data = response.json()
        self.__access_token: str = response_json_data.get('access_token')
        self.__token_type: str = response_json_data.get('token_type')
        self.__expires_in: int = int(response_json_data.get('expires_in'))
        self.__scope: str = response_json_data.get('scope')

    def get_access_token(self) -> str:
        return self.__access_token

    def get_token_type(self) -> str:
        return self.__token_type

    def get_time_of_access_token_request(self):
        return self.__time_of_access_token_request

    def get_expires_in(self) -> int:
        return self.__expires_in

    def get_scope(self) -> str:
        return self.__scope

    def did_authenticate(self):
        return self.__did_authenticate

    def did_token_expire(self):
        when = self.get_time_of_access_token_request()
        then = self.get_expires_in()
        now = get_time_now()
        return get_future_time_of(when, then) < now

    def update(self) -> None:
        if not self.did_token_expire():
            return

        self.perform_authentication()
    pass
