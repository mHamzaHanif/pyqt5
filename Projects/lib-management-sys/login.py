import MySQLdb

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.uic import loadUiType
login,_ = loadUiType('login.ui')

from library import Library

class Login(QMainWindow , login):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        # self.set_image_background()
        self.theme()
        self.setFixedSize(self.size())
        
        # login button
        self.pushButton_login.clicked.connect(self.handle_login)
        self.shortcut = QShortcut(QKeySequence("return"), self)
        self.shortcut.activated.connect(self.handle_login)

    def set_image_background(self):
        oImage = QImage("icons/background.png")
        sImage = oImage.scaled(QSize(530,330))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)
        
    def theme(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
        self.center()
    
    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
                  
    def handle_login(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='password' , db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data  :
            if username == row[1] and password == row[3]:
                print('user match')
                self.hide()
                window2 = Library()
                window2.show()
                window2.exec_()

            else:
                self.lineEdit_username.setText('')
                self.lineEdit_password.setText('')
                QMessageBox.warning(self, 'Incorrect',
                                'Please fill all fields correctly',
                                QMessageBox.Ok)
                self.lineEdit_username.setFocus()
    
