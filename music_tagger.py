import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from spotify_search import get_artist_info
import requests
import os
import random


def get_artist_image_src(artist_name: str = None) -> str:
    """
    Retrieves Artist's image url,
    :param artist_name: name of the artist
    :return: url to the artist image
    :raise ValueError: when artist name is malformed, or info on artist image url; could not be found.
    """

    # region guard condition for: artist
    if artist_name is None:
        raise ValueError('Please provide artist name!')
    elif artist_name == '' or artist_name == ' ' * len(artist_name):
        raise ValueError('Please provide artist name!')
    # endregion guard condition for: artist

    artist_info = get_artist_info(artist_name)

    try:
        if artist_info is None:
            raise ValueError('could not retrieve, artist info!')
    except ValueError:
        return ''

    artist_image: dict = {}

    try:
        for image in artist_info.images:
            if image.get('height') < 640:
                continue
            artist_image = image
            break

        if not artist_image:
            raise ValueError('could not retrieve, artist image src!')
    except ValueError:
        return ''
    except AttributeError:
        return ''

    return artist_image.get('url')


def download_artist_image(artist_name: str = None, download_directory: str = None) -> bool:
    """
    Downloads the Artist's image.
    :param artist_name: name of the artist
    :param download_directory: full qualifying path, to the folder that contains audio files.
    :return: boolean flag indicating success of download
    :raise ValueError: when artist_name is Malformed, or when download_directory
     is None, blank, Malformed or does not exists.
    """

    # region guard condition for: artist_name and download_directory
    if artist_name is None:
        raise ValueError('Please provide artist name!')
    elif artist_name == '' or artist_name == ' ' * len(artist_name):
        raise ValueError('Please provide artist name!')

    if download_directory is None:
        raise ValueError('Please provide download_directory!')
    elif download_directory == '' or download_directory == ' ' * len(download_directory):
        raise ValueError('Please provide download_directory!')
    elif not os.path.exists(download_directory) or not os.path.isdir(download_directory):
        raise ValueError('Please provide a valid download_directory; that exists!')
    # endregion guard condition for: artist

    artist_image_src = get_artist_image_src(artist_name)                                                                    # url to download from

    # region pre-guard condition against Malformed artist_image_src
    if artist_image_src is None or artist_image_src == '' or artist_image_src == ' '*len(artist_image_src):
        return False
    # endregion pre-guard condition against Malformed artist_image_src

    artist_image_path = os.path.join(download_directory, 'artist.png')                                                      # file to be downloaded

    file_size = 0 if not os.path.exists(artist_image_path) else os.stat(artist_image_path).st_size                          # file size

    user_agent_list = [
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/57.0.2987.110 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/61.0.3163.79 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
         'Gecko/20100101 '
         'Firefox/55.0'),  # firefox
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/61.0.3163.91 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/62.0.3202.89 '
         'Safari/537.36'),  # safari
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/63.0.3239.108 '
         'Safari/537.36'),  # firefox agent
    ]                                                                                                 # web browser agent instances, firefox, chrome, safari

    headers = {
        "User-Agent": random.choice(user_agent_list),
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Range': f'bytes={file_size}-'
    }                                                                                                         # request header

    try:
        with requests.get(url=artist_image_src, headers=headers, stream=True) as artist_image_download:                     # issuing a download request
            if artist_image_download.ok and artist_image_download.status_code in range(200, 300):                           # check server response in range 200 - 299 (can download)
                download_file_size = int(artist_image_download.headers.get('Content-Length'))                               # get download file size
                if file_size < download_file_size:                                                                          # attempt to continue downloading, file size < original
                    try:
                        with open(artist_image_path, 'a+b') as downloaded_file:                                             # open or create new file in append byte mode
                            for chunk in artist_image_download.iter_content(chunk_size=1024):                               # get from server, 1 kilo bit chunk
                                downloaded_file.write(chunk)                                                                # append chunk to local file
                        return True
                    except PermissionError:
                        return False
                else:
                    return False
            else:
                return False
    except requests.exceptions.MissingSchema as url_error:
        return False


def tag_artist_image_to_mp3_file(folder: str = None, audio_file: str = None) -> bool:
    """
    Tag audio file: with artist image
    :param audio_file: audio file name
    :param folder: of the audio file
    :return boolean flag  True to indicate success
    :raise ValueError: when either folder nor audio_file are Malformed
    """

    # region guard condition for: folder and audio
    if audio_file is None:
        raise ValueError('Please provide audio file name!')
    elif audio_file == '' or audio_file == ' ' * len(audio_file):
        raise ValueError('Please provide audio file name!')

    if folder is None:
        raise ValueError('Please provide folder!')
    elif folder == '' or folder == ' ' * len(folder):
        raise ValueError('Please provide folder!')
    elif not os.path.exists(folder) or not os.path.isdir(folder):
        raise ValueError('Please provide a valid folder; that exists!')
    # endregion guard condition for: folder and audio

    audio_path = os.path.join(folder, audio_file)

    # region guard condition for : audio path
    if not os.path.exists(audio_path):
        raise ValueError('Provided audio file that does not exists!')
    elif not os.path.isfile(audio_path):
        raise ValueError('Provided an audio file pointing to a folder? uhm why..')
    # endregion guard condition for : audio path

    artist_image_path = os.path.join(folder, 'artist.png')

    try:
        audio = MP3(audio_path, ID3=ID3)

        # add ID3 tag if it doesn't exist
        try:
            audio.add_tags()
        except error:
            pass

        # read artist_image and tag it to audio
        try:
            audio.tags.add(APIC(
                encoding=3,  # 3 is for utf-8
                mime='image/png',  # image/jpeg or image/png
                type=3,  # 3 is for the cover image
                desc=u'Cover',
                data=open(artist_image_path, 'rb').read()
            ))
            audio.save()
            print(f'tagged artist.png to audio file {audio_file}!', end='\r')
            return True
        except FileNotFoundError:
            print('./artist.png does not exist...', end='\r')
            return False
    except mutagen.mp3.HeaderNotFoundError:
        print(f'cant tag artist.png to audio file! already tagged {audio_file}', end='\r')
        return False


def is_audio_file_tagged(folder, audio_file) -> bool:
    try:
        path = os.path.join(folder, audio_file)
        audio_tag = mutagen.File(path)
        return 'APIC:Cover' in audio_tag.keys()
    except mutagen.mp3.HeaderNotFoundError:
        return True


def perform_image_tag_for(artist_name: str = None, folder: str = None, audio_file: str = None):
    """
    Tags an artist's, image to an audio file, download artist.png to the folder
    """

    # region check if folder contains artist.png file
    path_of_artist_png_file = os.path.join(folder, 'artist.png')
    artist_png_file_exists = (os.path.exists(path_of_artist_png_file) and os.path.isfile(path_of_artist_png_file))
    # endregion check if folder contains artist.png file

    file_downloaded = True
    if not artist_png_file_exists:
        file_downloaded = download_artist_image(artist_name, download_directory=folder)

    if file_downloaded and not is_audio_file_tagged(folder, audio_file):
        tag_artist_image_to_mp3_file(folder, audio_file)
    pass

