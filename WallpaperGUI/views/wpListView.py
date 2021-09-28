from models.fileTreeModel import FileInfo, ImageInfo
import PySimpleGUI as gui
import os.path as Path
from json import dump, load

class WPListView:
   def __init__(self, settingsPath) -> None:
      self.wpList: list[ImageInfo] = []
      self.settingsPath = settingsPath
      self.selectedWP: FileInfo = None
      self.loadWPList(True)

   def loadWPList(self, initialLoad=False):
      try:
         if Path.isfile(self.settingsPath):
            if Path.splitext(self.settingsPath)[1] == '.pcl':
               with open(self.settingsPath, 'r') as file:
                  data = load(file)
                  self.wpList = []
                  for img in data:
                     self.wpList.append(ImageInfo(img))
               if not initialLoad:
                  self.updateList()
                  return True
         return False
      except Exception:
         return False

   def saveWPList(self, newPath: str = None):
      if newPath != None:
         self.settingsPath = newPath
         fileMode = 'x'
      else:
         fileMode = 'w'
      with open(self.settingsPath, fileMode) as file:
         output = []
         for wp in self.wpList:
            output.append(wp.fullPath)
         dump(output, file)

   def selectionChangedEvent(self, args):
      if len(args) > 0:
         for img in self.wpList:
            if img.name == args[0]:
               self.selectedWP = img
               return

   def removeSelectedEvent(self):
      if self.selectedWP != None:
         self.wpList.remove(self.selectedWP)
         self.updateList()

   def addFileEvent(self, file):
      tempImage = ImageInfo(file)
      if not self.wpList.__contains__(tempImage):
         for img in self.wpList:
            if img.fullPath == file:
               return
         self.wpList.append(tempImage)
      self.updateList()

   def loadListEvent(self):
      self.loadWPList()
   
   def saveListEvent(self):
      self.saveWPList()

   def clearEvent(self):
      self.wpList = []
      self.updateList()

   def updateList(self):
      self.listBox.update(self.setDisplayList())

   def setDisplayList(self):
      output = []
      for file in self.wpList:
         output.append(file.name)
      return output

   def create(self):
      self.listBox = gui.Listbox(
         self.setDisplayList(),
         key='wplist-view',
         enable_events=True,
         select_mode=gui.SELECT_MODE_SINGLE,
         size=(200, 400)
      )
      layout = [
         [gui.Button('Remove', key='remove-wp-list', enable_events=True, expand_x=True)],
         [gui.Button('Load', enable_events=True, key='load-wp-list'), gui.Button('Save', enable_events=True, key='save-wp-list'), gui.Button('Clear List', enable_events=True, key='clear-wp-list')],
         [self.listBox]
      ]
      self.frame = gui.Frame('Selected Wallpapers', layout, size=(300, 900))
      return self.frame