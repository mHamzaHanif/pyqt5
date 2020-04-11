from PyQt5 import QtWidgets

import sqlite3

import sys
sys.path.insert(0, '.')
from ui.SearchStudent import Ui_Dialog
import imgs_rc

class SearchStudent_addition(Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SearchStudent_addition, self).__init__(parent)
        self.setupUi(self)
        
        
        self.pushButton_search.clicked.connect(self.searchstudent)
        
        self.show()
    
    
    def searchstudent(self):
        searchrol = ""
        searchrol = self.lineEdit_Roll_no.text()
    
        
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT * from students WHERE roll_no="+str(searchrol))
            row = result.fetchone()
            serachresult = "Rollno : "+str(row[0])+'\n'+"Name : "+str(row[1])+'\n'+"Branch : "+str(row[2])+'\n'+"Semiater : "+str(row[3])+'\n'+"Address : "+str(row[4])
            QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(), 'Successful', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()


        except Exception:
           QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(), 'Error', 'Could not Find student from the database.')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    action = SearchStudent_addition()
    sys.exit(app.exec_())