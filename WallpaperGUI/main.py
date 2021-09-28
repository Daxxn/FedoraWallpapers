from views.mainWindow import MainWindow

def main() -> None:
   mainView = MainWindow()
   mainView.create()
   mainView.show()

if __name__ == '__main__':
   main()
else:
   print('File is not a module.')