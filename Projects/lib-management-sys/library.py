import datetime

from xlrd import *
from xlsxwriter import *

import MySQLdb

from xlrd import *
from xlsxwriter import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.uic import loadUiType
library, _ = loadUiType('library.ui')


class Library(QMainWindow, library):
    def __init__(self, parent=None):
        super(Library, self).__init__(parent)
        self.setupUi(self)
        self.handle_UI_changes()
        self.dark_orange_theme()
        self.setFixedSize(self.size())
        
        # Handle buttons
        self.handle_buttons()
        
        # Settings(4th tab) > Catagories (1st tab) + Author (2nd tab) + Publisher (3rd tab)
        self.show_catagory()
        self.show_author()
        self.show_publisher()
        
        # Book(2nd Tab) > Add new book tab(1st tab)
        self.show_catagory_comboBox()
        self.show_author_comboBox()
        self.show_publisher_comboBox()
        
        # Show results
        self.show_all_clients() # Clients
        self.show_all_books()   # Books
        self.show_all_operations()
        
    def handle_UI_changes(self):
        self.hiding_themes()
        self.tabWidget.tabBar().setVisible(False)
    
    def handle_buttons(self):
        # Themes
        self.pushButton_themeShow.clicked.connect(self.show_themes)
        self.pushButton_themeHide.clicked.connect(self.hiding_themes)
        
        self.pushButton_dark_orange_theme.clicked.connect(self.dark_orange_theme)
        self.pushButton_dark_gray_theme.clicked.connect(self.dark_gray_theme)
        self.pushButton_dark_blue_theme.clicked.connect(self.dark_blue_theme)
        self.pushButton_qdark_theme.clicked.connect(self.qdark_theme)
        
        # Day to day opearations
        self.pushButton_day_to_day.clicked.connect(self.open_day_to_day_tab)
        self.pushButton_dashboard_add.clicked.connect(self.handle_dashboard_operation)
        self.pushButton_dashboard_export.clicked.connect(self.export_day_operations)
        
        # Book
        self.pushButton_book.clicked.connect(self.open_book_tab)
        self.pushButton_add_new_book_save.clicked.connect(self.add_new_book)
        self.pushButton_book_export.clicked.connect(self.export_books)
        ## Book > Edit/Delete book (2nd tab)
        self.pushButton_search_book_title.clicked.connect(self.search_book)
        self.pushButton_book_edit_save.clicked.connect(self.edit_book)
        self.pushButton_book_delete.clicked.connect(self.delete_book)
        
        # Client 
        self.pushButton_clients.clicked.connect(self.open_client_tab)
        self.pushButton_add_new_client.clicked.connect(self.add_new_client)
        self.pushButton_search_client.clicked.connect(self.search_client)
        self.pushButton_save_client.clicked.connect(self.edit_client)
        self.pushButton_client_dalete.clicked.connect(self.delete_client)
        self.pushButton_clients_export.clicked.connect(self.export_clients)
        
        # User
        self.pushButton_users.clicked.connect(self.open_users_tab)
        self.pushButton_add_new_user.clicked.connect(self.add_new_user)
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_edit_user_data.clicked.connect(self.edit_user)
        
        # Settings
        self.pushButton_settings.clicked.connect(self.open_settings_tab)
        self.pushButton_add_new_catagory.clicked.connect(self.add_catagory)
        self.pushButton_add_new_author.clicked.connect(self.add_author)
        self.pushButton_add_new_publisher.clicked.connect(self.add_publisher)  
          
    ## Theme 
    def show_themes(self):
        self.groupBox_theme.show()
    
    def hiding_themes(self):
        self.groupBox_theme.hide()
        
    ##################################################################
    ######################## Opening Tab #############################
    def open_day_to_day_tab(self):
        self.tabWidget.setCurrentIndex(0)
        
    def open_book_tab(self):
        self.tabWidget.setCurrentIndex(1)
    
    def open_client_tab(self):
        self.tabWidget.setCurrentIndex(2)
    
    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(3)
    
    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(4)
    
    ##################################################################
    ########################### Dashboard ############################
    def show_all_operations(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' 
            SELECT book_name ,client ,type , date , to_date FROM dayoperations
        ''')
        data = self.cur.fetchall()

        self.tableWidget_dashboard.setRowCount(0)
        self.tableWidget_dashboard.insertRow(0)
        for row , form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget_dashboard.setItem(row , column , QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_dashboard.rowCount()
            self.tableWidget_dashboard.insertRow(row_position)

    def handle_dashboard_operation(self):
        book_name = self.lineEdit_dashboard_title.text()
        client = self.lineEdit_dashboard_client_name.text()
        type = self.comboBox_type.currentText()
        days = self.comboBox_days.currentIndex() + 1
        date = datetime.date.today()
        to_date =  date + datetime.timedelta(days=days)

        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO dayoperations(book_name,client,type,days,date,to_date)
            VALUES                   (%s       , %s    , %s  , %s   ,%s   ,%s)
        ''' ,                        (book_name, client, type, days ,date ,to_date))

        self.db.commit()
        self.statusBar().showMessage('New Operation Added')

        self.show_all_operations()
        
    ##################################################################
    ########################### Book #################################
    def show_all_books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        self.cur.execute(''' SELECT book_code,book_name,book_description,book_catagory,book_author, book_publisher,book_price FROM book''')
        data = self.cur.fetchall()
        
        self.tableWidget_book.setRowCount(0)
        self.tableWidget_book.insertRow(0)
        
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_book.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            
            row_position = self.tableWidget_book.rowCount()
            self.tableWidget_book.insertRow(row_position)
            
        self.db.close()
    
    def add_new_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        book_title = self.lineEdit_title.text()
        book_description = self.textEdit_add_new_book.toPlainText()
        book_code = self.lineEdit_code.text()
        book_catagory = self.comboBox_catagory.currentText() 
        book_author = self.comboBox_author.currentText()
        book_publisher = self.comboBox_publisher.currentText()
        book_price = self.lineEdit_price.text()
        
        self.cur.execute('''
                         INSERT INTO book(book_name,book_description,book_code,book_catagory,book_author,book_publisher,book_price)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (book_title,book_description,book_code,book_catagory,book_author,book_publisher,book_price))
        
        self.db.commit()
        self.statusBar().showMessage('New Book Added')
        
        # Reset everything 
        self.lineEdit_title.setText('')
        self.textEdit_add_new_book.setPlainText('')
        self.lineEdit_code.setText('')
        self.comboBox_catagory.setCurrentText(0) 
        self.comboBox_author.setCurrentText(0)
        self.comboBox_publisher.setCurrentText(0)
        self.lineEdit_price.setText('')
        
        self.show_all_books()
    
    def search_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_search_book_title.text()
        
        sql = ''' SELECT * FROM book WHERE book_name=%s'''
        self.cur.execute(sql, [(book_title)])
        data = self.cur.fetchone()
        self.show_all_books()
    
        # Displaying data into respective widgets
        self.lineEdit_book_title_editORdelete.setText(data[1])
        self.textEdit_editOrDelete_book.setPlainText(data[2])
        self.lineEdit_book_code_editORdelete.setText(data[3])
        self.comboBox_book_catagory_editORdelete.setCurrentText(data[4])
        self.comboBox_book_author_editORdelete.setCurrentText(data[5])
        self.comboBox_book_publisher_editORdelete.setCurrentText(data[6])
        self.lineEdit_book_price_editORdelte.setText(str(data[7]))
        
    def edit_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        book_title = self.lineEdit_book_title_editORdelete.text()
        book_description = self.textEdit_editOrDelete_book.toPlainText()
        book_code = self.lineEdit_book_code_editORdelete.text()
        book_catagory = self.comboBox_book_catagory_editORdelete.currentText() 
        book_author = self.comboBox_book_author_editORdelete.currentText()
        book_publisher = self.comboBox_book_publisher_editORdelete.currentText()
        book_price = self.lineEdit_book_price_editORdelte.text()
        
        search_book_title = self.lineEdit_search_book_title.text()
        self.cur.execute('''
                UPDATE book SET book_name=%s, book_description=%s, book_code=%s, book_catagory=%s, book_author=%s, book_publisher=%s, book_price=%s WHERE book_name = %s
        ''', (book_title, book_description, book_code, book_catagory, book_author, book_publisher, book_price, search_book_title))
        
        self.db.commit()
        self.statusbar.showMessage("Book Updated")
        
        self.show_all_books()
            
    def delete_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        book_title = self.lineEdit_search_book_title.text()
        
        warning = QMessageBox.warning(self, 'Deleting book',
                                       'Are you sure you want to delete this book',
                                        QMessageBox.Yes | QMessageBox.No)
        
        if warning == QMessageBox.Yes:
            sql = ''' DELETE FROM book WHERE book_name = %s '''
            self.cur.execute(sql, [(book_title)])
            self.db.commit()

            self.statusBar().showMessage('Book Removed')
            
            self.show_all_books()
        
    ##################################################################
    ########################### Clients ##############################
    def show_all_clients(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        self.cur.execute(''' SELECT client_name, client_email,client_nationalID FROM client ''')
        data = self.cur.fetchall()

        self.tableWidget_client.setRowCount(0)
        self.tableWidget_client.insertRow(0)
        
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_client.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            
            row_position = self.tableWidget_client.rowCount()
            self.tableWidget_client.insertRow(row_position)
            
        self.db.close()
    
    def add_new_client(self):
        client_name = self.lineEdit_add_new_client_name.text()
        client_email = self.lineEdit_add_new_client_email.text()
        client_id = self.lineEdit_add_new_client_id.text()
    
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''
                INSERT INTO client(client_name,client_email, client_nationalID)
                VALUES (%s, %s, %s)         
                ''', (client_name, client_email, client_id))
        self.db.commit()
        self.db.close()
        
        self.statusbar.showMessage("New Client Added")
        
        self.show_all_clients()
                    
    def search_client(self):
        client_nationalID = self.lineEdit_search_client.text()
        
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        sql = ''' SELECT *FROM client WHERE client_nationalID = %s '''
        self.cur.execute(sql, [(client_nationalID)])
        data = self.cur.fetchone()
        
        self.lineEdit_client_name.setText(data[1])
        self.lineEdit_client_email.setText(data[2])
        self.lineEdit_client_id.setText(data[3])
        
        self.show_all_clients()
    
    def edit_client(self):
        national_id_orginal  = self.lineEdit_search_client.text() # search
        
        client_name = self.lineEdit_client_name.text()
        client_email = self.lineEdit_client_email.text()
        client_id = self.lineEdit_client_id.text()
    
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''
                         UPDATE client SET client_name=%s ,client_email=%s ,client_nationalID=%s WHERE client_nationalID=%s
                         ''', (client_name, client_email, client_id, national_id_orginal))
        self.db.commit()
        
        self.statusBar().showMessage('Client Data Updated')
        
        self.show_all_clients()
        
    def delete_client(self):
        national_id_orginal  = self.lineEdit_search_client.text() # search

        warning_message = QMessageBox.warning(self, 'Delete Client', 'Do you want to delete client?', QMessageBox.Yes | QMessageBox.No)
        
        if warning_message == QMessageBox.Yes:
            self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
            self.cur = self.db.cursor()
            self.cur.execute('''
                    DELETE FROM client WHERE client_nationalID = %s 
            ''', [(national_id_orginal)])
            
            self.db.commit()
            self.db.close()
            
            self.statusBar().showMessage('Client Deleted')
            
            self.show_all_clients()

    ##################################################################
    ########################### Users ################################   
    def add_new_user(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='password' , db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_add_new_username.text()
        email = self.lineEdit_add_new_email.text()
        password = self.lineEdit_add_new_password.text()
        password2 = self.lineEdit_add_new_confirm_password.text()

        if password == password2 :
            self.cur.execute(''' 
                INSERT INTO users(user_name , user_email , user_password)
                VALUES (%s , %s , %s)
            ''' , (username , email , password))

            self.db.commit()
            
            self.statusBar().showMessage('New User Added')

        else:
            self.label_incorrect_passward.setText('*Please add a valid password twice')
            self.label_incorrect_passward.setStyleSheet('QLabel { color: red }')
                    
    def login(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='password' , db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_login_username.text()
        password = self.lineEdit_login_password.text()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()

        for row in data:
            if username == row[1] and password == row[3]:
                self.statusBar().showMessage('Valid Username & Password')
                self.groupBox_edit_user_data.setEnabled(True)

                self.lineEdit_edit_user_name.setText(row[1])
                self.lineEdit_edit_user_email.setText(row[2])
                # self.lineEdit_edit_user_data_password.setText(row[3])
                
    def edit_user(self):
        username = self.lineEdit_edit_user_name.text()
        email = self.lineEdit_edit_user_email.text()
        password = self.lineEdit_edit_user_data_password.text()
        password2 = self.lineEdit_edit_user_data_confirm_password.text()

        original_name = self.lineEdit_login_username.text() # from login

        if password == password2 :
            self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
            self.cur = self.db.cursor()
            self.cur.execute('''
                UPDATE users SET user_name=%s , user_email=%s , user_password=%s WHERE user_name=%s
            ''', (username , email , password , original_name))
            self.db.commit()
            
            self.statusBar().showMessage('User Data Updated Successfully')

        else:
            self.label_incorrect_passward_2.setText('*Please add a valid password twice')
            self.label_incorrect_passward_2.setStyleSheet('QLabel { color: red }')

    ##################################################################
    ########################### Settings #############################
    def add_catagory(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        catagory_name = self.lineEdit_enter_catagory.text()
        
        self.cur.execute('''
           INSERT INTO catagory (catagory_name) VALUES (%s)
        ''', (catagory_name,))
        self.db.commit()
        
        self.statusbar.showMessage("New Category Added")
        self.lineEdit_enter_catagory.setText('')
        
        self.show_catagory()
        self.show_catagory_comboBox()
        
    def show_catagory(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT catagory_name FROM catagory''')
        data = self.cur.fetchall()
        
        if data:
            self.tableWidget_catagories.setRowCount(0)
            self.tableWidget_catagories.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_catagories.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
            
                row_position = self.tableWidget_catagories.rowCount()
                self.tableWidget_catagories.insertRow(row_position)    
                
    def add_author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        author = self.lineEdit_enter_author.text()
        
        self.cur.execute('''
           INSERT INTO authors (author_name) VALUES (%s)
        ''', (author,))
        
        self.db.commit()
        self.lineEdit_enter_author.setText('')
        self.statusbar.showMessage("New Author Added")
        self.show_author()
        self.show_publisher()
        self.show_author_comboBox()
    
    def show_author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT author_name FROM authors''')
        data = self.cur.fetchall()
        
        if data:
            self.tableWidget_author.setRowCount(0)
            self.tableWidget_author.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_author.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
            
                row_position = self.tableWidget_author.rowCount()
                self.tableWidget_author.insertRow(row_position)  
    
    def add_publisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        publisher_name = self.lineEdit_enter_publisher.text()
        
        self.cur.execute('''
           INSERT INTO publisher (publisher_name) VALUES (%s)
        ''', (publisher_name,))
        
        self.db.commit()
        
        self.statusbar.showMessage("New Publisher Added")
        self.lineEdit_enter_publisher.setText('')
        
        self.show_publisher()
        self.show_publisher_comboBox()
    
    def show_publisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()
        
        if data:
            self.tableWidget_publisher.setRowCount(0)
            self.tableWidget_publisher.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_publisher.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
            
                row_position = self.tableWidget_publisher.rowCount()
                self.tableWidget_publisher.insertRow(row_position)  
    
    ##################################################################
    ################## #Show Settings Data in UI #####################
    def show_catagory_comboBox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT catagory_name FROM catagory''')
        data = self.cur.fetchall()
        
        self.comboBox_catagory.clear()
        for catagory in data:
            self.comboBox_catagory.addItem(catagory[0])
            self.comboBox_book_catagory_editORdelete.addItem(catagory[0])
    
    def show_author_comboBox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT author_name FROM authors''')
        data = self.cur.fetchall()
        
        self.comboBox_author.clear()
        for author in data:
            self.comboBox_author.addItem(author[0])
            self.comboBox_book_author_editORdelete.addItem(author[0])
    
    def show_publisher_comboBox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()
        
        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()
        
        self.comboBox_publisher.clear()
        for publisher in data:
            self.comboBox_publisher.addItem(publisher[0])
            self.comboBox_book_publisher_editORdelete.addItem(publisher[0])
            
    ##################################################################
    ########################### Exprt Data ########################### 
    def export_day_operations(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' 
            SELECT book_name , client , type , date , to_date FROM dayoperations
        ''')

        data = self.cur.fetchall()
        wb = Workbook('day_operations.xlsx')
        sheet1  = wb.add_worksheet()

        sheet1.write(0,0,'book title')
        sheet1.write(0,1,'cliant name')
        sheet1.write(0,2,'type')
        sheet1.write(0,3,'from - date')
        sheet1.write(0,4,'to - date')


        row_number = 1
        for row in data :
            column_number = 0
            for item in row :
                sheet1.write(row_number , column_number , str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage('Report Created Successfully')
    
    def export_books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT book_code,book_name,book_description,book_catagory,book_author,book_publisher,book_price FROM book''')
        data = self.cur.fetchall()

        wb = Workbook('all_books.xlsx')
        sheet1 = wb.add_worksheet()

        sheet1.write(0,0 , 'Book Code')
        sheet1.write(0,1 , 'Book Name')
        sheet1.write(0,2 , 'Book Description')
        sheet1.write(0,3 , 'Book Category')
        sheet1.write(0,4 , 'Book Author')
        sheet1.write(0,5 , 'Book publisher')
        sheet1.write(0,6 , 'Book Price')


        row_number = 1
        for row in data :
            column_number = 0
            for item in row :
                sheet1.write(row_number , column_number , str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage('Book Report Created Successfully')

    def export_clients(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='password', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT client_name , client_email ,client_nationalID FROM client ''')
        data = self.cur.fetchall()

        wb = Workbook('all_client.xlsx')
        sheet1 = wb.add_worksheet()

        sheet1.write(0,0 , 'Client Name')
        sheet1.write(0,1 , 'CLient Email')
        sheet1.write(0,2 , 'CLient natioanalID')


        row_number = 1
        for row in data :
            column_number = 0
            for item in row :
                sheet1.write(row_number , column_number , str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage('client Report Created Successfully')

    ##################################################################
    ############################# UI Themes ##########################
    def dark_blue_theme(self):
        style = open('themes/darkblue.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_gray_theme(self):
        style = open('themes/darkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_orange_theme(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def qdark_theme(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
 