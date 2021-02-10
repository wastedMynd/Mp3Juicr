from music_tagger import perform_image_tag_for
import glob
import os
from posix import DirEntry
from threading import Thread


def preform_task(m_folder, m_artist):
    search_files_on_path = os.path.join(m_folder, '*.mp3')
    for path in glob.glob(pathname=search_files_on_path):
        file = os.path.basename(path)
        perform_image_tag_for(
            artist_name=m_artist,
            folder=m_folder,
            audio_file=file
        )
    pass


def process_entry(m_entry):
    for instance in os.scandir(m_entry):
        try:
            directory: DirEntry = instance
            if not directory.is_dir():
                continue

            folder = directory.path

            artist_folder = os.path.basename(folder)
            artist = artist_folder.replace('_', ' ').title()

            process = Thread(target=preform_task, args=(folder, artist))
            process.start()

        except Exception:
            continue


base = '/home/sizwe/Downloads/mp3juices'
entries: list = [
    base,
    os.path.join(base, 'fav'),
    os.path.join(base, 'Hip pop'),
    os.path.join(base, 'new recommendations'),
]

for entry in entries:
    process_entry_thread = Thread(target=process_entry, args=(entry,))
    process_entry_thread.start()
