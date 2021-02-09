import argparse
import shutil
import os
import youtube_search

from moviepy.editor import VideoFileClip
from pytube import YouTube

DEFAULT_SONGS_FILE_PATH = 'songs.txt'
BASE_YOUTUBE_URL = 'https://www.youtube.com'
URL_KEY = 'url_suffix'


def download_song_from_url(url: str, output_dir: str) -> None:
    """
    This function download song from youtube
    :param url: The url in youtube that play the song
    :param output_dir: The path to directory that we want to download the song to
    :return: the name of the downloaded song
    """
    mp4 = YouTube(url).streams.get_highest_resolution().download()
    mp3 = mp4.split(".mp4", 1)[0] + '.mp3'
    mp3 = output_dir + '\\' + os.path.basename(mp3)

    video_clip = VideoFileClip(mp4)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(mp3)

    audio_clip.close()
    video_clip.close()

    os.remove(mp4)


def get_url_from_song_name(song_name: str) -> str:
    """
    This function return the url in youtube that play the selected song
    :param song_name: The name of the selected song
    :return: The url of the selected song
    """
    results = youtube_search.YoutubeSearch(song_name).to_dict()
    return BASE_YOUTUBE_URL + results[0][URL_KEY]


def get_list_of_songs(songs_file_path: str) -> list:
    """
    This function gets the list of songs that we want to download
    :param songs_file_path: The path to the file that contains the songs
    :return: List of songs to download
    """
    songs = []
    with open(songs_file_path, 'rb') as song_file:
        all_songs = song_file.read().split(b'\n')
    for song in all_songs:
        songs.append(song.decode())
    return songs


def main(args):

    songs = get_list_of_songs(args.input_file)
    for song in songs:
        try:
            url = get_url_from_song_name(song)
            download_song_from_url(url, args.output_dir)
            print(f"Successfully download song: {song}")
        except Exception as e:
            print(f"Can't download song: {song} with error: {e}, continue to next song")


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Downloads songs from youtube')
    arg_parser.add_argument('--songs_file_path', '-fp', dest='input_file', type=str, default=DEFAULT_SONGS_FILE_PATH,
                            help='The path to the file that contains the songs')
    arg_parser.add_argument('--dir_path', '-dp', dest='output_dir', type=str, default=os.path.curdir,
                            help='The path the folder that will contains the downloaded songs')
    main(arg_parser.parse_args())
