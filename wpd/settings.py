import os
import os.path as Path
from pickle import Pickler, Unpickler

settingsPath = '/home/Daxxn/Pictures/wallpaperSettings.pcl'
class Settings:
   def __init__(self) -> None:
      self.bashScript: str = None
      self.wpListPath: str = None
      self.enabled: bool = None
      self.randomEnable: bool = None
      self.interval: int = None
      self.currentIndex: int = 0

   @staticmethod
   def loadSettings():
      try:
         if Path.isfile(settingsPath):
            with open(settingsPath, 'rb') as file:
               pickle = Unpickler(file)
               return pickle.load()
      except Exception as e:
         print(str(e))

   def saveSettings(self):
      try:
         if Path.isfile(settingsPath):
            with open(settingsPath, 'wb') as file:
               pickle = Pickler(file)
               pickle.dump(self)
      except Exception as e:
         print(str(e))
    