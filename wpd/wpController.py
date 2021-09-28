from json.decoder import JSONDecoder
import os.path as path
import os
from json import JSONEncoder, JSONDecoder
from random import randrange as random

bashScript = 'gsettings set org.gnome.desktop.background picture-uri "file://{0}"'
wpListPath = '/home/Daxxn/Pictures/wallpaperList.json'

def readWPFile():
    result = []
    with open(wpListPath, 'r') as file:
        decoder = JSONDecoder()
        result = decoder.decode(file.read())
        print(result)
    return result

def changeWallpaper(manualSelect: int = None):
    try:
        wpFiles = readWPFile()
        if manualSelect == None:
            fileName = wpFiles[random(0, len(wpFiles))]
        else:
            fileName = wpFiles[manualSelect]
        if path.exists(fileName):
            print('Attempting wp change.')
            os.system(bashScript.format(fileName))
            print('Change made.')
        else:
            print('File not found.')
    except Exception as e:
        print(str(e))