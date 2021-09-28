import os.path as Path
import os
from pickle import Pickler, Unpickler

class SettingsModel:
   def __init__(self, enabled: bool, enableRandom: bool, wpListPath: str, interval: int) -> None:
      self.enabled = enabled
      self.enableRandom = enableRandom
      self.wpListPath = wpListPath
      self.interval = interval

class DefaultSettings:
   def __init__(self) -> None:
      self.enabled = True
      self.enableRandom = False
      self.wpListPath = '/home/Daxxn/Pictures/wallpaperList.json'
      self.interval = 20

class SettingsManager:
   def __init__(self, settingsPath) -> None:
      self.settingsPath = settingsPath if len(settingsPath) > 0 else '/home/Daxxn/Pictures'
      self.settings: SettingsModel = None

   def copy(self, settings: SettingsModel):
      self.settings = SettingsModel(
         settings.enabled,
         settings.enableRandom,
         settings.wpListPath,
         settings.interval
      )

   def loadSettings(self):
      try:
         if Path.isfile(self.settingsPath):
            with open(self.settingsPath, 'rb') as file:
               pickler = Unpickler(file)
               self.settings = pickler.load()
            return True
         else:
            return False
      except Exception:
         return False

   def saveSettings(self):
      if Path.isfile(self.settingsPath):
         with open(self.settingsPath, 'wb') as file:
            pickler = Pickler(file)
            pickler.dump(self.settings)

   def __str__(self):
      return '{0}\t{1}\t{2}\t{3}\t{4}'.format(self.Enabled, self.EnableRandom, self.Interval, self.WPListPath, self.Hash)

   @property
   def Hash(self):
      wpListHash = 0
      byt = bytearray(self.WPListPath, 'utf-8')
      for i in range(len(byt)):
         wpListHash += i + byt[i]
      return self.Interval + self.Enabled + self.EnableRandom + wpListHash

   @property
   def Enabled(self):
      return self.settings.enabled
   @Enabled.setter
   def Enabled(self, value: bool):
      self.settings.enabled = value
   
   @property
   def EnableRandom(self):
      return self.settings.enableRandom
   @EnableRandom.setter
   def EnableRandom(self, value: bool):
      self.settings.enableRandom = value

   @property
   def WPListPath(self):
      return self.settings.wpListPath
   @WPListPath.setter
   def WPListPath(self, value: str):
      self.settings.wpListPath = value

   @property
   def Interval(self):
      return self.settings.interval
   @Interval.setter
   def Interval(self, value: int):
      self.settings.interval = value
   