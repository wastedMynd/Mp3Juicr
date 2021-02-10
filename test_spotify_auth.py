import spotify_auth
import pytest


def test_client_id() -> None:
    assert spotify_auth.get_client_id() is not None, 'Spotify client_id is None'
    pass


def test_client_secret() -> None:
    assert spotify_auth.get_client_secret() is not None, 'Spotify client_secret is None'
    pass


def test_client_credentials() -> None:
    assert spotify_auth.get_client_credentials() is not None, 'Spotify client_credentials is None'
    pass


def test_client_credentials_encoded() -> None:
    assert spotify_auth.get_client_credentials_encoded() is not None, 'Spotify client_credentials_encoded is None'
    pass


def test_client_credentials_encoded_as_base64() -> None:
    assert spotify_auth.get_client_credentials_encoded_as_base64() is not None,\
        'Spotify client_credentials_encoded_as_base64 is None'
    pass


def test_client_credentials_decode() -> None:
    assert spotify_auth.get_client_credentials_decode() is not None, 'Spotify client_credentials_decode is None'
    pass


def test_client_token_url() -> None:
    assert spotify_auth.get_client_token_url() is not None, 'Spotify client_token_url is None'
    pass


def test_client_token_data() -> None:
    assert spotify_auth.get_client_token_data() is not None, 'Spotify client_token_data is None'
    pass


def test_client_token_header() -> None:
    assert spotify_auth.get_client_token_header() is not None, 'Spotify client_token_header is None'
    pass


def test_auth_response() -> None:
    test_response = spotify_auth.get_auth_response()
    assert test_response is not None, 'Spotify aut response is None'
    assert spotify_auth.check_if_response_is_good(test_response), 'Spotify auth response is bad'

    test_response_json: dict = test_response.json()
    assert test_response_json is not None, 'Spotify aut response_json is None'

    keys = ['access_token', 'token_type', 'expires_in']

    @pytest.mark.parametrize('key', keys)
    def test_response_json_keys(key) -> None:
        assert key in test_response_json.keys(), f'Spotify aut response_json does not contain key {key}'

    for r_key in keys: test_response_json_keys(r_key)
    pass


class MockResponse(object):
    def __init__(self, ok, status_code):
        self.ok = ok
        self.status_code = status_code


@pytest.mark.parametrize('response', [MockResponse(ok=True, status_code=200)])
def test_check_if_response_is_good(response) -> None:
    assert spotify_auth.check_if_response_is_good(response), 'Spotify auth response is bad'
    pass


def test_spotify_authenticate_client() -> None:
    spotify_authenticate_client = spotify_auth.SpotifyAuthenticateClient()
    assert spotify_authenticate_client is not None, 'Spotify Authenticate Client None'

    access_token = spotify_authenticate_client.get_access_token()
    assert access_token is not None, 'Spotify access_token is None'
    assert len(access_token) == 83, 'Spotify access_token length is not 83'

    token_type = spotify_authenticate_client.get_token_type()
    assert token_type is not None, 'Spotify token_type is None'
    assert token_type == 'Bearer', 'Spotify token_type is not Bearer'

    expires_in = spotify_authenticate_client.get_expires_in()
    assert expires_in is not None, 'Spotify expires_in is None'
    assert expires_in == 3_600, 'Spotify expires_in is not 3600'
    pass
