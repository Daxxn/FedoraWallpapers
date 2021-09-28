from uuid import UUID, uuid4 as uid
import os.path as Path
import os
import PySimpleGUI as gui

allowedExtensions = [
   '.png',
   '.jpg',
   '.bmp',
   '.jpeg',
   '.PNG'
]

iconsFolder = '/home/Daxxn/Code/Python/Projects/WallpaperManager/WallpaperGUI/icons'
folderIconName = 'FolderSmall.png'
fileIconName = 'FileSmall.png'

class FileInfo:
   def __init__(self, path: str = None, parentId: UUID = None) -> None:
      exists = Path.exists(path)
      if exists:
         self.id = uid()
         self.parentId = parentId
         self.isFile = Path.isfile(path)
         self.name: str = Path.basename(path)
         self.fullPath: str = path
         self.children: list[FileInfo] = []
         self.ext: str = ''
         self.isImage: bool = self.checkExt(path)
         if not self.isFile:
            self.populateChildren(path)
         else:
            self.ext: str = Path.splitext(path)[1]

   def populateChildren(self, rootDir: str):
      if Path.isdir(rootDir):
         paths = os.listdir(rootDir)
         for path in paths:
            temp = FileInfo(Path.join(rootDir, path), self.id)
            self.children.append(temp)
      else:
         return

   @staticmethod
   def checkExt(file: str):
      if Path.isfile(file):
         if allowedExtensions.__contains__(Path.splitext(file)[1]):
            return True
      return False

   def getChildrenIds(self):
      output = []
      for ch in self.children:
         output.append(ch.id)
      return output

   def searchTree(self, id: UUID):
      if str(self.id) == id:
         return self
      if len(self.children) > 0:
         for child in self.children:
            result = child.searchTree(id)
            if result != None:
               return result
      else:
         return None

   def setNodes(self, node: gui.TreeData):
      if node == None:
         node = gui.TreeData()
      node.insert(
         str(self.parentId) if self.parentId != None else '',
         str(self.id),
         self.name,
         [self.ext],
         icon=Path.join(iconsFolder, fileIconName) if self.isFile else Path.join(iconsFolder, folderIconName)
      )
      for child in self.children:
         child.setNodes(node)
      return node

   def getChild(self, id: UUID):
      output = None
      for ch in self.children:
         if id == ch.id:
            output = ch
            break
      return output

   @property
   def Name(self):
      return self.name

   @property
   def FullPath(self):
      return self.fullPath

   @property
   def AllowedExt():
      return [
         '.png',
         '.jpg',
         '.bmp',
         '.jpeg',
         '.PNG'
      ]

class ImageInfo:
   def __init__(self, path: str) -> None:
      if Path.isfile(path):
         self.fullPath = path
         self.name = Path.basename(path)