
from PyQt6.QtWidgets import QWidget, QMessageBox

from client_menu import ClientWindow
from db import dao
from gen.auth_window import Ui_Auth_Form
from menu import MenuWidow


class AuthWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Auth_Form()
        self.ui.setupUi(self)
        self.main_window = None
        self.__conn()

    def __conn(self):
        self.ui.pushButton_guest.clicked.connect(self.guest)
        self.ui.pushButton_login.clicked.connect(self.login)

    def login(self):
        login = self.ui.lineEdit_login.text().strip()
        password = self.ui.lineEdit_password.text().strip()
        print(login, password)
        if not password or not login:
            QMessageBox.warning(self, "лох", "заполни оба поля")
            return
        user = dao.login(login, password)

        if not user:
            QMessageBox.warning(self, "мне неприятно", "нет такого")
            return


        if user["role_id"] == 1:
            self.main_window = MenuWidow()
            self.main_window.show()
            self.close()

        if user["role_id"] == 2:
            self.client_window = ClientWindow(user["user_id"])
            self.client_window.show()
            self.close()


    def guest(self):
        self.main_window = MenuWidow()
        self.main_window.show()
        self.close()

        self.main_window.ui.pushButton_add.hide()
        self.main_window.ui.pushButton_edit.hide()
        self.main_window.ui.pushButton_delete.hide()
