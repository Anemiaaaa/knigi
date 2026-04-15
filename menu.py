from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QDialog, QMessageBox, QInputDialog

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
        self.load_orders()


    def insert_card(self):
        # Очищаем старые карточки
        while self.ui.verticalLayout_4.count():
            item = self.ui.verticalLayout_4.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        books = dao.get_all_books()

        for book in books:
            card = CardWindow(book)
            card.clicked.connect(self.najal)
            self.ui.verticalLayout_4.addWidget(card)

    def najal(self, book):
        self.selected = book

    # коннектим функцию
    def __conn(self):
        self.ui.pushButton_add.clicked.connect(self.add_book)
        self.ui.pushButton_edit.clicked.connect(self.edit_book)
        self.ui.pushButton_delete.clicked.connect(self.delete_book)
        self.ui.tableView.doubleClicked.connect(self.change_status)


    # грузим все заказы
    def load_orders(self):
        self.all_orders = dao.get_all_orders()

        self.ui.comboBox.clear()
        self.ui.comboBox.addItem("Все заказы")
        self.ui.comboBox.addItem("new")
        self.ui.comboBox.addItem("done")
        self.ui.comboBox.addItem("cancelled")

        # коннектим комбо бокс
        self.ui.comboBox.currentIndexChanged.connect(self.filter_orders)
        self.show_orders(self.all_orders)


    # фильтруем согласно комбо боксу
    def filter_orders(self):
        status = self.ui.comboBox.currentText()
        if status == "Все заказы":
            self.show_orders(self.all_orders)
        else:
            filtered = [o for o in self.all_orders if o["order_status"] == status]
            self.show_orders(filtered)

    # передаем сюда после фильтра и оно отображает
    def show_orders(self, orders):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID", "Пользователь", "Сумма", "Дата", "Статус"])

        for o in orders:
            row = [
                QStandardItem(str(o["order_id"])),
                QStandardItem(str(o["username"])),
                QStandardItem(str(o["total_sum"])),
                QStandardItem(str(o["order_date"])),
                QStandardItem(str(o["order_status"])),
            ]
            model.appendRow(row)

        self.ui.tableView.setModel(model)
        self.ui.tableView.resizeColumnsToContents()


    # добавить удалить редактироать для книги
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

    def change_status(self, index):
        row = index.row()
        model = self.ui.tableView.model()
        order_id = int(model.item(row, 0).text())  # колонка 0 = ID


        status, ok = QInputDialog.getItem(
            self, "Статус", "Выбери статус:",
            ["new", "done", "cancelled"], editable=False
        )

        if ok:
            dao.update_order_status(order_id, status)
            self.load_orders()

