import os
import subprocess
from multiprocessing import Pool
from tqdm import tqdm

def get_all_urls(playlist_url:str):
    command = ['yt-dlp', '--get-url', '--flat-playlist', playlist_url]
    output = subprocess.check_output(command, universal_newlines=True)
    video_links = output.strip().split("\n")
    return video_links


def download_single_audio(code = None):
    # Prepare the youtube video link
    video_link = f"https://www.youtube.com/watch?v={code}"
    save_dir = "~/Music/POP-ENG/"

    os.makedirs(save_dir, exist_ok=True)

    command = ['yt-dlp',
               '--audio-quality','0',
               '-x',
               '--audio-format', 'mp3',
               '-o', f'~/Music/POP-ENG/%(title)s.%(ext)s',
               video_link]
    

   # Download and save audio file from video file
    try: 
        subprocess.call(command)
    except Exception as ex:
        print("Exception Happened\n", str(ex))

    
 

def get_all_unique_codes(playlist_link_file):
    with open(playlist_link_file, "r") as fp:
        links = [x.rstrip() for x in fp.readlines() if x != ""]

        video_codes = []

        for link in links:
            print(link)
            
            try:
                video_links = get_all_urls(playlist_url = link)
                codes = [x.split("=")[-1] for x in video_links]
                print("Number of Video Links Found: ", len(codes))
                video_codes.extend(codes)
            except Exception as ex:
                print("Exception Happened")
                print(str(ex))
        
        return list(set(video_codes))




if __name__ == "__main__":
    codes = get_all_unique_codes("playlist_links.txt")
    num_threads = 4





    with Pool(num_threads) as pool:
        results = list(tqdm(pool.imap(download_single_audio, codes), 
                            total=len(codes)))
        with open("download_log.txt", "w") as fp:
            print(results, file=fp)

    




















    