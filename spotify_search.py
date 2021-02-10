from spotify_auth import SpotifyAuthenticateClient
import os
from urllib.parse import urlencode
import requests
import pprint
"""
search, artist from Spotify api 
"""


class AccessError(Exception):
    pass


spotify_auth = SpotifyAuthenticateClient()


# region helper methods

def __can_access_spotify() -> bool:
    tries = 2
    tried = 0
    successful = spotify_auth.did_authenticate() and not spotify_auth.did_token_expire()

    while not successful and tried < tries:
        try:
            if not spotify_auth.did_authenticate():
                raise AccessError(f'Spotify Authentication failed: tried = {tried + 1} of {tries}!')
            elif spotify_auth.did_token_expire():
                raise AccessError(f'Spotify Access Token expired: tried = {tried + 1} of {tries}!')
            else:
                successful = True
                print(f'Spotify already, authenticated!', end='\r')
                break
        except AccessError as error:
            tried += 1
            print(error)
            spotify_auth.update()
            successful = spotify_auth.did_authenticate() and not spotify_auth.did_token_expire()
            if successful:
                print(f'Spotify authenticated!', end='\r')
                break

    return successful


def __check_access_to_spotify():
    if not __can_access_spotify():
        raise AccessError("can't access Spotify at this time...")

# endregion


# region request methods

def get_spotify_search_url():
    return os.path.join(os.environ.get('SPOTIFY_BASE_URL'), 'search')


def get_spotify_header():
    return {'Authorization': f'Bearer {spotify_auth.get_access_token()}'}


def get_spotify_search_query_for(query, query_type: str):
    return urlencode({
        'q': query,
        'type': query_type.lower()
    })

# endregion


def search_artist_info(artist_name: str = None) -> dict:

    if artist_name is None:
        raise ValueError('provide an artist name')

    __check_access_to_spotify()

    spotify_query = get_spotify_search_query_for(query=artist_name, query_type='artist')

    query_url = f'{get_spotify_search_url()}?{spotify_query}'

    try:
        with requests.get(url=query_url, headers=get_spotify_header()) as response:
            return response.json()
    except Exception:
        return {}
    pass


def get_artist_info(artist_name:str = None, print_return=False):
    if artist_name is None:
        raise ValueError('provide an artist name')

    data = search_artist_info(artist_name)

    if 'artists' not in data.keys():
        return None

    artists = data.get('artists')

    item_count: int = artists.get('total')
    items: list = artists.get('items')

    artist_item: dict = {}

    for index in range(item_count):

        if index >= len(items):
            break

        item: dict = items[index]
        name: str = item.get('name')
        images: dict = item.get('images')

        if name == artist_name and len(images) > 0:
            artist_item = item
            break
    try:
        if len(artist_item) == 0:
            raise ValueError('artist not found!')
    except ValueError as error:
        try:
            artist_item = items[0]
        except IndexError:
            return None

    spotify_artist_info = SpotifyArtistInfo(artist_item)

    if print_return:
        pprint.pprint(spotify_artist_info.__str__())

    return spotify_artist_info


class SpotifyArtistInfo(object):
    def __init__(self, artist_item: dict = None):

        if artist_item is None:
            raise ValueError('artist_item is empty!')

        self.genres: list = artist_item.get('genres')  # :str
        self.images: list = artist_item.get('images')  # :dict
        self.popularity: int = artist_item.get('popularity')
        self.followers: dict = artist_item.get('followers')
        self.id: str = artist_item.get('id')
        self.name: str = artist_item.get('name')
        self.type_: str = artist_item.get('type')
        self.uri: str = artist_item.get('uri')
        self.href: str = artist_item.get('href')
        self.external_urls: dict = artist_item.get('external_urls')

    def __str__(self):
        return f"""
        genres:{self.genres},
        images:{self.images},
        popularity:{self.popularity},
        followers:{self.followers},
        id:{self.id},
        name:{self.name},
        type_:{self.type_},
        uri:{self.uri},
        href:{self.href},
        external_urls:{self.external_urls},
        """.strip()

