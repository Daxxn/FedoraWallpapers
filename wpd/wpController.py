import os.path as path
import os
from json import load
from random import randrange as random
from settings import SettingsModel
from LocalLogging.localLogger import Logger


def readFiles(settings: SettingsModel):
    wpList: list[str] = []
    with open(settings.wpListPath, 'r') as file:
        wpList = load(file)
    return wpList

def changeWallpaper(logger: Logger, settings: SettingsModel):
    try:
        wpList = readFiles(settings)
        if settings.enabled:
            if settings.enableRandom:
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
        return settings.stopDaemon
    except Exception as e:
        logger.error(e, 'Wallpaper change error.')