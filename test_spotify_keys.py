import pytest
import os


spotify_keys = ['SPOTIFY_CLIENT_SECRET', 'SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_TOKEN_URL', 'SPOTIFY_BASE_URL']


@pytest.mark.parametrize("key", spotify_keys)
def test_spotify_key(key):
    value = os.environ.get(key)
    assert value is not None, f'On .env file, Spotify key {key} is undefined!'
    assert len(value) > 0, f'On .env file, Spotify key {key} is empty!'
    assert value != ' '*len(value), f'On .env file, Spotify key {key} is blank!'
    pass
