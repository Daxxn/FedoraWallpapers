from models.settingsManager import SettingsManager
import PySimpleGUI as gui

class SettingsWindow:
   def __init__(self, settings: SettingsManager) -> None:
      self.settingsManager = settings
      self.settingsManager.copy(settings.settings)
      self.window: gui.Window = None
      self.currentHash = settings.Hash
      self.firstCloseAttempt = False
      self.create()

   def create(self):
      self.listFileTextBox = gui.Input(
         self.settingsManager.settings.wpListPath,
         enable_events=True,
         key='list-text'
      )
      self.enabledCheckBox = gui.Checkbox(
         'Enable Cycler',
         default=self.settingsManager.Enabled,
         enable_events=True,
         key='enabled-check'
      )
      self.randomCheckBox = gui.Checkbox(
         'Enable Randomize',
         default=self.settingsManager.EnableRandom,
         enable_events=True,
         key='enable-random-check'
      )
      self.intervalTextBox = gui.Input(
         self.settingsManager.Interval,
         enable_events=True,
         key='interval-text'
      )
      self.saveMessageText = gui.Text(
         'Some settings arent saved. close anyway?',
         visible=self.firstCloseAttempt
      )
      layout = [
         [self.enabledCheckBox],
         [self.randomCheckBox],
         [self.listFileTextBox],
         [self.intervalTextBox],
         [gui.Button('Save & Exit', key='save-settings', enable_events=True)],
         [self.saveMessageText]
      ]
      self.window = gui.Window(
         'Settings',
         layout,
         enable_close_attempted_event=True,
         force_toplevel=True,
         resizable=False,
         size=(250,300)
      )

   def show(self):
      while True:
         event, values = self.window.read()
         print(event)

         if event == gui.WIN_CLOSED or event == 'Cancel':
            break;

         elif event == 'list-text':
            self.settingsManager.WPListPath = values[event]

         elif event == 'enabled-check':
            self.settingsManager.Enabled = values[event]

         elif event == 'enable-random-check':
            self.settingsManager.EnableRandom = values[event]

         elif event == 'interval-text':
            try:
               num = int(values[event])
               self.settingsManager.Interval = num
               self.intervalTextBox.update(self.settingsManager.Interval)
            except Exception:
               self.intervalTextBox.update(self.settingsManager.Interval)
               print('Oops. Must be a number.')
               
         elif event == 'save-settings':
            try:
               self.settingsManager.saveSettings()
               break
            except Exception as e:
               print(str(e))

         if event == gui.WINDOW_CLOSE_ATTEMPTED_EVENT:
            print('in window close')
            newHash = self.settingsManager.Hash
            print(self.currentHash)
            print(newHash)
            if self.currentHash != newHash:
               if not self.firstCloseAttempt:
                  self.firstCloseAttempt = True
               else:
                  break
            else:
               break
         else:
            self.firstCloseAttempt = False
         
         self.saveMessageText.update(visible=self.firstCloseAttempt)

      self.window.close()