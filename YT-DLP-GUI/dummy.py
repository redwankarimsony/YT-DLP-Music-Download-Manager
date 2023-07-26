from pytube import YouTube

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # replace with your YouTube video url
youtube = YouTube(url)

# Get all available streams for the video
streams = youtube.streams

# Print all available video qualities
print()
for stream in streams:
    if stream.type == "video" or stream.type == "audiovisual":
        print(stream)

    if stream.type == "audio":
        print("audio", stream)


YouTube('https://youtu.be/9bZkp7q19f0').streams.first().download()