from PyQt5 import QtWidgets
from addition.action_MainWindowForm import MainWindowForm_addition
from addition.action_AddStudent import AddStudent_action

import imgs_rc
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()

    # p = MainWindowForm_addition(MainWindow)
    p = MainWindowForm_addition()
    # p.setupUi(MainWindow)
    # p.pr()
    # MainWindow.show()
    sys.exit(app.exec_())
