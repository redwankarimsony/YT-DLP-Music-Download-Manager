# YT-DLP-Music-Download-Manager

YT-DLP-Music-Download-Manager is a wrapper around YT-DLP that allows you to download music files in MP3 format with the highest audio quality in the shortest possible time. The main advantage of this tool is that it utilizes multithreading to maximize the utilization of your machine's resources for parallel song downloads.

## Dependencies

To use YT-DLP-Music-Download-Manager, you need to install the following dependencies:

1. Python 3.6 or higher
2. `yt-dlp` package: You can install it via `pip` using the command:
   ```
   pip install yt-dlp
   ```
3. `ffmpeg` package: You can install it via the following command (for Linux):
   ```
   sudo apt install ffmpeg
   ```
   Installing FFmpeg is essential for storing the music files in MP3 format. Without it, the files will be stored in `.webm` format.

## How to Use It

### Step 1: Clone the Repository

Clone the YT-DLP-Music-Download-Manager repository by running the following command in your terminal:
```
git clone https://github.com/redwankarimsony/YT-DLP-Music-Download-Manager.git
```

### Step 2: Navigate to the Repository

Change your current directory to the cloned repository:
```
cd YT-DLP-Music-Download-Manager
```

### Step 3: Add Playlist Links

Add all the playlists that you want to download to the `playlist_links.txt` file. Each playlist link should be on a separate line.

### Step 4: Download Music

Run the download script using the following command:
```
python download_script.py
```

This will initiate the music download process using YT-DLP-Music-Download-Manager. The script will fetch the playlist links from the `playlist_links.txt` file and download the music files in MP3 format with the highest audio quality.

Enjoy your downloaded music files!
