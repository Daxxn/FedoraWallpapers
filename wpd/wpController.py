import os.path as path
import os
from pickle import Unpickler
from random import randrange as random
from settings import Settings
from LocalLogging.logger import Logger


def readFiles():
    settings = Settings()
    settings.loadSettings()
    wpList: list[str] = []
    with open(settings.wpListPath, 'rb') as file:
        pickle = Unpickler(file)
        wpList = pickle.load()
    return (settings, wpList)

def changeWallpaper(logger: Logger):
    try:
        settings, wpList = readFiles()
        if settings.enabled:
            if settings.randomEnable == None:
                fileName = wpList[random(0, len(wpList))]
            else:
                fileName = wpList[settings.currentIndex]
                settings.currentIndex += 1
            if path.exists(fileName):
                logger.log('Attempting wp change.')
                status = os.system(settings.bashScript.format(fileName))
                if status == 0:
                    logger.log('Change made.')
                else:
                    logger.warn('Bash execution return an error.', status, settings.bashScript.format(fileName))
            else:
                logger.log('File not found.')
        else:
            logger.log('Wallpaper Daemon Disabled.')
    except Exception as e:
        print(str(e))