from PyQt5 import QtWidgets

import sqlite3

import sys

sys.path.insert(0, '.')
from ui.AddStudent import Ui_Dialog
import imgs_rc

class AddStudent_addition(Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddStudent_addition, self).__init__(parent)
        self.setupUi(self)
        
        self.pushButton_addStudent.clicked.connect(self.addstudent)

        self.show()
        
    def addstudent(self):
        rollno = ""
        name = ""
        branch = ""
        semister = -1
        address = ""

        rollno = self.lineEdit_roll_no.text()
        name = self.lineEdit_name.text()
        branch = self.comboBox_branch.itemText(self.comboBox_branch.currentIndex())
        semister = self.comboBox_branch.itemText(self.comboBox_branch.currentIndex())
        address = self.lineEdit_address.text()
        

        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO students (roll_no,name,branch,semister,address) VALUES (?,?,?,?,?)",(int(rollno), name, branch, semister, address))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Successful','Student is added successfully to the database.')
            self.close()
            
        except Exception:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(), 'Error', 'Could not add student to the database.')
        
        
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    action = AddStudent_addition()
    sys.exit(app.exec_())