from models.settingsManager import DefaultSettings, SettingsManager, SettingsModel
from uuid import uuid4
from views.settingsWindow import SettingsWindow
import PySimpleGUI as gui
from views.fileTreeView import FileTreeView
from views.wpListView import WPListView
from models.fileModels import *
from models.fileTreeModel import FileInfo
from models.imageConverter import convertImage

class MainWindow:
   def __init__(self) -> None:
      self.window = None
      self.filemanager = FileManager()
      self.selectedFile: FileInfo = None
      self.fileTree = FileTreeView()
      self.fileTreeView: gui.Tree = None
      self.imageView = gui.Image()
      self.imageSize: tuple[int, int] = (1000, 860)
      self.rootDir: FileInfo = None
      self.currentSettings: SettingsManager = None

   def openDir(self):
      try:
         directory = gui.filedialog.askdirectory(initialdir='~/Pictures', mustexist=True, title='Open Pictures Folder')

         self.rootDir = FileInfo(directory)

         self.treeData = self.rootDir.setNodes(gui.TreeData())
         self.fileTree.setTreeData(self.treeData)
      except Exception as e:
         print(str(e))

   def setImage(self):
      if self.selectedFile.isFile:
         if FileInfo.checkExt(self.selectedFile.fullPath):
            self.imageView.update(convertImage(self.selectedFile.fullPath, self.imageSize))

   def findSelection(self, ids):
      if len(ids) > 0:
         if ids[0] == 'None':
            return
         self.selectedFile = self.rootDir.searchTree(ids[0])

   def create(self):
      self.currentSettings = SettingsManager('/home/Daxxn/Pictures/wallpaperSettings.json')
      success = self.currentSettings.loadSettings()
      self.wpView = WPListView(
         self.currentSettings.settings.wpListPath if success else '/home/Daxxn/Pictures/wallpaperList.json'
      )
      self.imageView = gui.Image(size=self.imageSize)
      self.fileTreeView = self.fileTree.create()
      menu = [
         ['File', ['save default', '---', 'Save::save-settings']]
      ]
      imageColLayout = [
         [self.imageView]
      ]
      layout = [
         [gui.Menu(menu)],
         [self.fileTreeView, gui.Column(imageColLayout, scrollable=True, size=self.imageSize), self.wpView.create()]
      ]
      self.window = gui.Window('Wallpaper Setup', layout, finalize=True, size=(1800, 900), resizable=False)

   def show(self):
      while True:
         event, values = self.window.read()
         print(event)
         print(values)

         if event == gui.WIN_CLOSED or event == 'Cancel':
            break;

         elif event == 'tree-view':
            self.findSelection(values[event])
            if self.selectedFile != None:
               print(self.selectedFile.Name)
               # try:
               self.setImage()
               # except Exception as e:
               #    print(str(e))

         elif event == 'add-selected-file':
            if self.selectedFile != None and self.selectedFile.isImage:
               self.wpView.addFileEvent(self.selectedFile.fullPath)

         elif event == 'wplist-view':
            self.wpView.selectionChangedEvent(values[event])

         elif event == 'remove-wp-list':
            self.wpView.removeSelectedEvent()

         elif event == 'load-wp-list':
            self.wpView.loadListEvent()

         elif event == 'save-wp-list':
            self.wpView.saveListEvent()

         elif event == 'open-folder':
            self.openDir()

         elif event == 'open-settings':
            settingsWindow = SettingsWindow(self.currentSettings)
            settingsWindow.show()
            print(self.currentSettings)

         elif event == 'save default':
            self.currentSettings.settings = DefaultSettings()
            self.currentSettings.saveSettings()
         
         elif event == 'Save::save-settings':
            try:
               self.currentSettings.saveSettings()
            except Exception as e:
               print(str(e))

      self.window.close()