# YT-DLP-Music-Download-Manager
This is a wrapper around YT-DLP to download all the music files in mp3 format with the highest audio quality in shortest possible time. The main perk here is that it uses multithreading to use maximum amount of resource from your machine to download songs parallaly. 

## Dependencies
All you need is to install yt-dlp, python and ffmpeg
1. Python 3.6 or higher
2.  `yt-dlp`
   Install it via ```pip install yt-dlp```
3. `ffmpeg`
   Install it via ```sudo apt install ffmpeg``` Without it, music will be stored in `.webm` format


## How to Use It
### Step 1: Clone the repo 
Go to your terminal and run the following command to clone the repo in your machine.
```
git clone https://github.com/redwankarimsony/YT-DLP-Music-Download-Manager.git
```
### Step 2: Change your current location inside the repo.

``` cd YT-DLP-Music-Download-Manager ```

### Step 3: Add the playlist links
Add all the playlists that you want to download into the `playlist_links.txt` file

### Step 4: Download Music
Run the download script using the following command.
```python download_script.py```
