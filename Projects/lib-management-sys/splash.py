import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.uic import loadUiType
splash,_ = loadUiType('splash.ui')

from login import Login

class ThreadProgress(QThread):
    mysignal = pyqtSignal(int)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def run(self):
        i = 0
        while i<101:
            time.sleep(0.1)
            self.mysignal.emit(i)
            i += 1


class Splash(QMainWindow, splash):
    def __init__(self, parent = None):
        super(Splash, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setWindowFlags(Qt.SplashScreen|Qt.FramelessWindowHint)
        self.setupUi(self)
        pixmap = QPixmap("icons/test.png")
        self.splah_image.setPixmap(pixmap.scaled(350, 300))
        progress = ThreadProgress(self)
        progress.mysignal.connect(self.progress)
        progress.start()
        
    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        if i == 100:
            self.hide()
            login = Login(self)
            login.show()

