from settings import SettingsModel
import sys
import daemon
import time
from wpController import changeWallpaper
from LocalLogging.localLogger import Logger

def parseArgs():
    sys.argv
    if len(sys.argv) == 2:
        if sys.argv[1].strip() == 'debug':
            return True
        else:
            return False
    else:
        return False

def runDaemon(extLogger: Logger):
    extLogger.log('Starting Daemon...', True)
    with daemon.DaemonContext():
        while True:
            try:
                logger = Logger.startupLogger(extLogger.name)
                settings = SettingsModel.loadSettings(logger)
                changeWallpaper(logger, settings)
                settings.saveSettings(logger)
                if settings.stopDaemon:
                    break
                time.sleep(settings.interval)
            except Exception as e:
                logger.error(e, 'main execution failure.')

def runDebug(logger: Logger):
    settings = SettingsModel.loadSettings(logger)
    changeWallpaper(logger, settings)
    settings.saveSettings(logger)

def main(debugMode: bool) -> None:
    logger = Logger.startupLogger('wpd', debugMode)
    # settings = SettingsModel.loadSettings(logger)
    # if settings != None:
    if not debugMode:
        runDaemon(logger)
        logger.log('Stopping Daemon', True)
    else:
        logger.log('Running in debug mode', True)
        runDebug(logger)
    #     settings.saveSettings(logger)
    logger.saveLogFile()

if __name__ == '__main__':
    debugMode = parseArgs()
    main(debugMode)
else:
    print('File is not a module.')