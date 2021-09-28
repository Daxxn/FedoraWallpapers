import os.path as Path
import os
from json import dump, load

class SettingsModel:
   def __init__(self, bashScript: str, enabled: bool, enableRandom: bool, wpListPath: str, interval: int, stopDaemon: bool) -> None:
      self.bashScript = bashScript
      self.wpListPath = wpListPath
      self.enabled = enabled
      self.enableRandom = enableRandom
      self.interval = interval
      self.currentIndex = 0
      self.stopDaemon = stopDaemon

class DefaultSettings:
   def __init__(self) -> None:
      self.bashScript = 'gsettings set org.gnome.desktop.background picture-uri "file://{0}"'
      self.enabled = True
      self.enableRandom = False
      self.wpListPath = '/home/Daxxn/Pictures/wallpaperList.pcl'
      self.interval = 20
      self.currentIndex = 0
      self.stopDaemon = True

class SettingsManager:
   def __init__(self, settingsPath) -> None:
      self.settingsPath = settingsPath if len(settingsPath) > 0 else '/home/Daxxn/Pictures'
      self.settings: SettingsModel = None

   def copy(self, settings: SettingsModel):
      self.settings = SettingsModel(
         settings.bashScript,
         settings.enabled,
         settings.enableRandom,
         settings.wpListPath,
         settings.interval,
         settings.stopDaemon
      )

   def loadSettings(self):
      try:
         if Path.isfile(self.settingsPath):
            with open(self.settingsPath, 'r') as file:
               data = load(file)
               self.settings = SettingsModel(
                  data['bashScript'],
                  data['enabled'],
                  data['enableRandom'],
                  data['wpListPath'],
                  data['interval'],
                  data['stopDaemon']
               )
            return True
         else:
            return False
      except Exception:
         return False

   def saveSettings(self):
      if Path.isfile(self.settingsPath):
         with open(self.settingsPath, 'w') as file:
            output = {
               'bashScript': self.settings.bashScript,
               'enabled': self.settings.enabled,
               'enableRandom': self.settings.enableRandom,
               'wpListPath': self.settings.wpListPath,
               'interval': self.settings.interval,
               'stopDaemon': self.settings.stopDaemon
            }
            dump(output, file)

   def __str__(self):
      return '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(
         self.Enabled,
         self.EnableRandom,
         self.StopDaemon,
         self.Interval,
         self.WPListPath,
         self.Hash
      )

   @property
   def Hash(self):
      wpListHash = 0
      byt = bytearray(self.WPListPath, 'utf-8')
      for i in range(len(byt)):
         wpListHash += i + byt[i]
      return self.Interval + self.Enabled + self.EnableRandom + wpListHash + self.StopDaemon

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

   @property
   def StopDaemon(self):
      return self.settings.stopDaemon
   @StopDaemon.setter
   def StopDaemon(self, value: bool):
      self.settings.stopDaemon = value
   
   @property
   def BashScript(self):
      return self.settings.bashScript
   