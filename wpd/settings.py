import os
import os.path as Path
from json import load, dump
from typing import Any
from LocalLogging.localLogger import Logger

settingsPath = '/home/Daxxn/Pictures/wallpaperSettings.pcl'

class SettingsModel:
   def __init__(self) -> None:
      self.bashScript: str = None
      self.enabled: bool = None
      self.enableRandom: bool = None
      self.wpListPath: str = None
      self.interval: int = None
      self.currentIndex: int = 0
      self.stopDaemon = False

   def fromDict(self, data: dict[str, Any]):
      for k in data.keys():
         setattr(self, k, data[k])

   def __setattr__(self, name: str, value: Any) -> None:
      self.__dict__[name] = value

   @staticmethod
   def loadSettings(logger: Logger):
      try:
         if Path.isfile(settingsPath):
            with open(settingsPath, 'r') as file:
               data = load(file)
               temp = SettingsModel()
               temp.fromDict(data)
               return temp
      except Exception as e:
         logger.error(e, 'Setting file load error.')

   def saveSettings(self, logger: Logger):
      try:
         if Path.isfile(settingsPath):
            with open(settingsPath, 'w') as file:
               output = {
                  'bashScript': self.bashScript,
                  'enabled': self.enabled,
                  'enableRandom': self.enableRandom,
                  'wpListPath': self.wpListPath,
                  'interval': self.interval,
                  'currentIndex': self.currentIndex,
                  'stopDaemon': self.stopDaemon
               }
               dump(output, file)
      except Exception as e:
         logger.error(e, 'Setting file save error.')
    