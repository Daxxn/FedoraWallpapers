import PySimpleGUI as gui

class FileTreeView:
   def __init__(self) -> None:
      self.frame = None
      self.data: gui.TreeData = None

   def setTreeData(self, data: gui.TreeData):
      self.data = data
      self.tree.update(self.data)

   def initTreeData(self):
      treedata = gui.TreeData()
      treedata.Insert("", 'None', 'None', ['',''])
      return treedata

   def create(self) -> gui.Frame:
      self.tree = gui.Tree(
         self.initTreeData(),
         headings=['Ext'],
         key='tree-view',
         enable_events=True,
         expand_y=True,
         max_col_width=35,
         col_widths=[5],
         auto_size_columns=False,
         col0_width=35
      )
      layout = [
         [gui.Button('Open Folder', key='open-folder', expand_x=True)],
         [gui.Button('Settings', enable_events=True, key='open-settings', expand_x=True)],
         [gui.Button('Add Selected', enable_events=True, expand_x=True, key='add-selected-file')],
         [self.tree]
      ]

      self.frame = gui.Frame('Files', layout, size=(600, 900), expand_y=True)
      return self.frame