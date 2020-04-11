from PySide2 import QtWidgets

from ui import main

class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)
        self.showMaximized()
        self.setWindowTitle("My Qt Application")
        self.pushButton.clicked.connect(self.fill_form)
        
    def fill_form(self):
        name = self.lineEdit.text()
        email = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        if (not name) or (not email) or (not password):
            QtWidgets.QMessageBox.about(self, "Field Required!", "Please! Fill the form properly.")
            return
        else:
            QtWidgets.QMessageBox.about(self, "Success", "Done.")
            return
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication()
    qt_app = MyQtApp()
    qt_app.show()
    app.exec_()