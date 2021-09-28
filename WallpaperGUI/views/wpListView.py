from models.fileTreeModel import FileInfo, ImageInfo
import PySimpleGUI as gui
import os.path as Path
from json import JSONDecoder, JSONEncoder

class WPListView:
   def __init__(self, settingsPath) -> None:
      self.wpList: list[ImageInfo] = []
      self.settingsPath = settingsPath
      self.selectedWP: FileInfo = None
      self.loadWPList(True)

   def loadWPList(self, initialLoad=False):
      if Path.isfile(self.settingsPath):
         if Path.splitext(self.settingsPath)[1] == '.json':
            with open(self.settingsPath, 'r') as file:
               decoder = JSONDecoder()
               data = decoder.decode(file.read())
               self.wpList = []
               for img in data:
                  self.wpList.append(ImageInfo(img))
            if not initialLoad:
               self.updateList()

   def saveWPList(self, newPath: str = None):
      if newPath != None:
         self.settingsPath = newPath
         fileMode = 'x'
      else:
         fileMode = 'w'
      with open(self.settingsPath, fileMode) as file:
         encoder = JSONEncoder(indent=3)
         file.write(encoder.encode(self.wpList))

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
      print()

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
         [gui.Button('Remove', key='remove-wp-list', expand_x=True)],
         [gui.Button('Load', key='load-wp-list'), gui.Button('Save', key='save-wp-list')],
         [self.listBox]
      ]
      self.frame = gui.Frame('Selected Wallpapers', layout, size=(300, 900))
      return self.frame