from PyQt6.QtWidgets import QWidget, QDialog, QMessageBox

from add_edit import AddEditWindow
from card import CardWindow
from db import dao
from gen.main_window import Ui_Main_Form


class MenuWidow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main_Form()
        self.ui.setupUi(self)
        self.__conn()
        self.card = None
        self.selected = None
        self.insert_card()


    def insert_card(self):
        books = dao.get_all_books()

        for book in books:
            card = CardWindow(book)
            card.clicked.connect(self.najal)
            self.ui.verticalLayout_4.addWidget(card)

    def najal(self, book):
        self.selected = book


    def __conn(self):
        self.ui.pushButton_add.clicked.connect(self.add_book)
        self.ui.pushButton_edit.clicked.connect(self.edit_book)
        self.ui.pushButton_delete.clicked.connect(self.delete_book)

    def add_book(self):
        self.add_edit_window = AddEditWindow()
        if self.add_edit_window.exec() == QDialog.DialogCode.Accepted:
            author, book_name, price, discount, image = self.add_edit_window.get()

            image = image.split("/")[-1].split(".")[0]
            dao.insert_book(book_name, price, author, image, discount)
            self.insert_card()
            QMessageBox.information(self, "ВСЕ ЧЕТКО", "ДОБАВИЛОСЬ")

    def edit_book(self):
        if not self.selected:
            QMessageBox.warning(self, "Нужно выбрать книгу", "Сначала кликни по карточке книги.")
            return

        self.add_edit_window = AddEditWindow(self.selected)
        if self.add_edit_window.exec() == QDialog.DialogCode.Accepted:
            author, book_name, price, discount, image = self.add_edit_window.get()

            image = image.split("/")[-1].split(".")[0]
            dao.edit_book(self.selected["book_id"], book_name, price, author, image, discount)
            self.insert_card()
            QMessageBox.information(self, "ВСЕ ЧЕТКО", "РЕДАКТИРОВАЛОСЬ")

    def delete_book(self):
        if not self.selected:
            QMessageBox.warning(self, "Нужно выбрать книгу", "Сначала кликни по карточке книги.")
            return

        dao.delete_book(self.selected["book_id"])
        self.insert_card()
        QMessageBox.information(self, "ВСЕ ЧЕТКО", "УДАЛИЛОСЬ")
