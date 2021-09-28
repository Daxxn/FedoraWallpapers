from uuid import uuid4 as uid
import os.path as Path
import os

class FileInfo:
   def __init__(self, path: str = None) -> None:
      exists = Path.exists(path)
      if exists:
         self.id = uid()
         self.isFile = Path.isfile(path)
         self.name: str = Path.basename(path)
         self.fullPath: str = path

class FileManager:
   def __init__(self, rootDir: str = Path.curdir) -> None:
      self.rootDir: str = rootDir
      self.files: list[FileInfo] = []

   def openDir(self, dir: str = None):
      if dir != None:
         self.rootDir = dir
      if Path.isdir(self.rootDir):
         paths = os.listdir(self.rootDir)
         for path in paths:
            self.files.append(FileInfo(path))

   def clear(self):
      self.rootDir = None
      self.files = None