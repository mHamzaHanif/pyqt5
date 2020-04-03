# Importing libraries
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Window"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

# sys.argv parameter is a list of arguments from a command line.
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())