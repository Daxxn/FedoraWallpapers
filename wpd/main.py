import sys
import daemon
import time
from wpController import changeWallpaper

def parseArgs():
    sys.argv
    if sys.argv[0].strip() == 'debug':
        return True
    else:
        return False

def runDaemon():
    print('Starting Daemon...')
    with daemon.DaemonContext():
        while True:
            changeWallpaper()
            time.sleep(15)

def runDebug():
    changeWallpaper()

def main(debugMode: bool) -> None:
    if debugMode:
        # runDaemon()
        print('run daemon')
    else:
        runDebug()

if __name__ == '__main__':
    debugMode = parseArgs()
    main(debugMode)
else:
    print('File is not a module.')