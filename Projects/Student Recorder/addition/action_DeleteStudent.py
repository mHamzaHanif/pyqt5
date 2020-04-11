from PyQt5 import QtWidgets

import sqlite3

import sys
sys.path.insert(0, '.')
from ui.DeleteStudent import Ui_Dialog
import imgs_rc

class DeleteStudent_addition(Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DeleteStudent_addition, self).__init__(parent)
        
        # Code here
        self.setupUi(self)
        
        self.pushButton_delete.clicked.connect(self.deletestudent)

        self.show()

    def deletestudent(self):
        del_rollno = ""
        del_rollno = self.pushButton_delete.text()
        
        
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("DELETE from students WHERE roll_no="+str(del_rollno))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Successful','Deleted From Table Successful')
        self.close()
        
        # try:
        #     self.conn = sqlite3.connect("database.db")
        #     self.c = self.conn.cursor()
        #     self.c.execute("DELETE from students WHERE roll_no="+str(del_rollno))
        #     self.conn.commit()
        #     self.c.close()
        #     self.conn.close()
        #     QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Successful','Deleted From Table Successful')
        #     self.close()
            
        # except Exception:
        #     QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(), 'Error', 'Could not Delete student from the database.')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = DeleteStudent_addition()
    sys.exit(app.exec_())
