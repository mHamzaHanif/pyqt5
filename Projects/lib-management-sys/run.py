import time
import datetime

from xlrd import *
from xlsxwriter import *

import MySQLdb

from xlrd import *
from xlsxwriter import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from library import Library
from login import Login
from splash import Splash

def main():
    app = QApplication(sys.argv)
    # window = Library()
    # window = Login()
    window = Splash() 
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()