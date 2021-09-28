import sys
import daemon
import time
from wpController import changeWallpaper
sys.path.append('/home/Daxxn/Code/Python/Libraries')
from  import Logger

def parseArgs():
    sys.argv
    if sys.argv[0].strip() == 'debug':
        return True
    else:
        return False

def runDaemon(logger: Logger):
    logger.log('Starting Daemon...')
    with daemon.DaemonContext():
        while True:
            changeWallpaper()
            time.sleep(15)

def runDebug():
    changeWallpaper()

def main(debugMode: bool) -> None:
    if debugMode:
        logger = Logger('wpd')
        # runDaemon(logger)
        print('run daemon')
    else:
        logger = Logger('wpd-debug')
        runDebug()

if __name__ == '__main__':
    debugMode = parseArgs()
    main(debugMode)
else:
    print('File is not a module.')