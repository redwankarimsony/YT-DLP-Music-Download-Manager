import re
import requests
import os

def is_valid_youtube_playlist(link):
    # Check if the link matches the YouTube playlist URL pattern
    # playlist_regex = r'^https:\/\/www.youtube.com\/playlist\?list=([a-zA-Z0-9_-]+)'
    # match = re.match(playlist_regex, link)
    # if not match:
    #     print("Not a valid YouTube Playlist Link")
    #     return False

    # Perform a request to the link and check the response
    response = requests.get(link)
    if response.status_code == 200 and "youtube.com/playlist" in response.url:
        # The link is a valid YouTube playlist
        print("Valid YouTube Playlist Link Found")
        return True
    else:
        # The link is not a valid YouTube playlist
        print("Not a valid YouTube Playlist Link Found")
        return False