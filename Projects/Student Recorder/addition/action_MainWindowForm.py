from PyQt5 import QtWidgets
from PyQt5 import QtGui

import sqlite3

import sys
import time
import os

sys.path.insert(0, '.')
from ui.MainWindowForm import Ui_MainWindow
from action_AddStudent import AddStudent_addition
from action_SearchStudent import SearchStudent_addition
from action_DeleteStudent import DeleteStudent_addition

import imgs_rc
# from MainWindowForm import Ui_MainWindow 

class MainWindowForm_addition(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindowForm_addition, self).__init__(parent)
        QtWidgets.qApp.installEventFilter(self)
        self.setupUi(self)
    
        # self.showMaximized()
        self.setWindowTitle("Student Management System")
        self.setWindowIcon(QtGui.QIcon('Pg2.png'))  #window icon
        
        # SQLite3
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS students(roll_no TEXT,name TEXT,branch TEXT,semister INTEGER,address TEXT)") # INTEGER PRIMARY KEY AUTOINCREMENT
        self.c.close()

        
        # Actions
        ## Menu
        self.actionClose.triggered.connect(self.menu_Close)
        self.actionAuthor.triggered.connect(self.menu_Author)
        
        ## Toolbar
        self.actionAdd_Student.triggered.connect(self.toolbar_add_student)
        self.actionReferesh.triggered.connect(self.toolbar_Refresh)
        self.actionFind.triggered.connect(self.toolbar_Find)
        self.actionDelete.triggered.connect(self.toolbar_Delete)
        
        self.show()

    def loaddata(self):
        self.connection = sqlite3.connect("database.db")
        query = "SELECT * FROM students"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    # Actions
    ## Menu
    def menu_Close(self):
        print("Close")
        
    def menu_Author(self):
        print("Author")
    
    ## Toolbar
    def toolbar_add_student(self): ## Error
        dialog = QtWidgets.QDialog
        action = AddStudent_addition()
        dialog.exec_()
        
    def toolbar_Refresh(self):
        print("Refresh")
        self.loaddata()
        
    def toolbar_Find(self):
        print("Search")
        dialog = QtWidgets.QDialog
        action = SearchStudent_addition()
        dialog.exec_()
        
    def toolbar_Delete(self):
        print("Delete")
        dialog = QtWidgets.QDialog
        action = DeleteStudent_addition()
        dialog.exec_()
    

        
app = QtWidgets.QApplication(sys.argv)
if (QtWidgets.QDialog.Accepted == True):
    win = MainWindowForm_addition()
    win.show()
    win.loaddata()
sys.exit(app.exec_())



