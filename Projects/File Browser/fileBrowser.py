from PySide2 import QtWidgets ,QtGui, QtCore
import os, sys, subprocess


from ui import main

class MyFileBrowser(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyFileBrowser, self).__init__()
        self.setupUi(self)
        self.showMaximized()
        self.setWindowTitle("My File Broweser")
        # self.pushButton.clicked.connect(self.fill_form)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.populate()
        
        
    def populate(self):
        path = "/home"
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)
        
    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open")
        open.triggered.connect(self.open_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())
        
        
    def open_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
    
        # For windows
        if sys.platform == "win32": 
            os.startfile(file_path)
        # For Linux
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file_path])
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    qt_app = MyFileBrowser()
    qt_app.show()
    app.exec_()