import youtube_dl
import os
import sys
from mutagen.mp3 import EasyMP3 as MP3
from gmusicapi import Musicmanager

def initializeClient():
    client = Musicmanager()

    if (client.login()):
        return client
    else:
        client.perform_oauth(open_browser=True)
        initializeClient()

def uploadFile(fileName: str):
    client.upload("./" + fileName)
    os.remove("./" + fileName)

def downloadVideo(url: str):
    ydl_opts = {
    'format': 'bestaudio/best',
    'forcefilename': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }]
}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        if (ydl.download([url]) == 0):
            filename = list(filter(lambda x: x.endswith(".mp3"), os.listdir(".")))[0]
            processFile(filename)

def processFile(fileName: str):
    file = MP3("./" + fileName)
    file["title"] = sys.argv[3]
    file["artist"] = sys.argv[2]

    if (len(sys.argv) >= 5):
        file["album"] = sys.argv[4]

    file.save()

    uploadFile(fileName)

client = initializeClient()
downloadVideo(sys.argv[1])