import os
import subprocess
from multiprocessing import Pool
from tqdm import tqdm

import eyed3
from PIL import Image
import glob


__all__ = ["get_all_unique_codes", "download_single_audio", "get_all_urls", "embedd_audio"]


def get_all_urls(playlist_url: str):
    command = ['yt-dlp', '--get-url', '--flat-playlist', playlist_url]
    output = subprocess.check_output(command, universal_newlines=True)
    video_links = output.strip().split("\n")
    return video_links


def download_single_audio(link=None, code=None):
    # Prepare the youtube video link
    if link is not None:
        video_link = link
    elif code is not None:
        video_link = f"https://www.youtube.com/watch?v={code}"

    save_dir = "~/Music/CarSongs/"

    os.makedirs(save_dir, exist_ok=True)

    command = ['yt-dlp',
               '--write-thumbnail',
               '--audio-quality', '0',
               '-x',
               '--audio-format', 'mp3',
               '-o', f'~/Music/CarSongs/%(title)s.%(ext)s',
               video_link]

    # Download and save audio file from video file
    try:
        output = subprocess.run(command)
        print(output.returncode)
    except Exception as ex:
        print("Exception Happened\n", str(ex))


def get_all_unique_codes(playlist_link_file):
    with open(playlist_link_file, "r") as fp:
        links = [x.rstrip() for x in fp.readlines() if x != ""]

        video_codes = []

        for link in links:
            print(link)

            try:
                video_links = get_all_urls(playlist_url=link)
                codes = [x.split("=")[-1] for x in video_links]
                print("Number of Video Links Found: ", len(codes))
                video_codes.extend(codes)
            except Exception as ex:
                print("Exception Happened")
                print(str(ex))

        return list(set(video_codes))


def embedd_audio(audio_file_path, thumbnail_path=None):
    # Load the MP3 audio file
    # audio_file_path = '1.mp3'
    audio = eyed3.load(audio_file_path)

    # Specify the path to the thumbnail image file
    if thumbnail_path is None:
        thumbnail_path = audio_file_path.replace(".mp3", ".webp")
        img = Image.open(thumbnail_path).convert("RGB")
        new_thumbnail_path = thumbnail_path.replace(".webp", ".jpg")
        img.save(new_thumbnail_path)

    # Convert The Thumbnail

    # Set the thumbnail image
    audio.tag.images.set(3, open(new_thumbnail_path, 'rb').read(), 'image/jpeg')

    # Save the modified audio file
    audio.tag.save()


if __name__ == "__main__":
    codes = get_all_unique_codes("car_songs.txt")

    num_threads = os.cpu_count() - 2

    with Pool(num_threads) as pool:
        results = list(tqdm(pool.imap(download_single_audio, codes),
                            total=len(codes)))
        with open("download_log.txt", "w") as fp:
            print(results, file=fp)

    mp3_files = glob.glob("../CarSongs/*.mp3")

    for mp3_file in mp3_files:
        try:
            embedd_audio(mp3_file)
        except:
            print("Something went wrong for ", mp3_file)
