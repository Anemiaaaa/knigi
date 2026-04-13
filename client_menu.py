from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QMessageBox

from card_client import ClientCardWindow
from db import dao
from gen.client_window import Ui_Main_Form


class ClientWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.ui = Ui_Main_Form()
        self.ui.setupUi(self)

        self.user_id = user_id
        self.my_orders = dao.get_orders_by_user_id(self.user_id)

        # модель для таблицы заказов
        self.order_model = QStandardItemModel()
        self.order_model.setHorizontalHeaderLabels(["Название", "Автор", "Цена"])
        self.ui.tableView_order_items.setModel(self.order_model)

        # карточки книг
        self.books = dao.get_all_books()
        self.insert_card(self.books)

        # фильтр по авторам
        self.authors = dao.get_all_authors()
        self.ui.comboBox_2.addItem("Все")
        self.ui.comboBox_2.addItems(author["author"] for author in self.authors)
        self.ui.pushButton_find.clicked.connect(self.search)

        # фильтр заказов по статусам
        self.ui.comboBox_status.addItem("Все")
        self.ui.comboBox_status.addItem("new")
        self.ui.comboBox_status.addItem("done")
        self.ui.comboBox_status.addItem("cancelled")
        self.ui.pushButton_status.clicked.connect(self.filter_status)

        # кнопка оформить заказ
        self.ui.pushButton_order.clicked.connect(self.confirm_order)

        # грузим заказы
        self.load_client_orders()

    def insert_card(self, books):
        for book in books:
            card = ClientCardWindow(book)
            card.clicked.connect(self.add_order_item)

            self.ui.verticalLayout_4.addWidget(card)

    def add_order_item(self, book):
        row = [
            QStandardItem(book["book_name"]),
            QStandardItem(book["author"]),
            QStandardItem(str(book["price"])),
            QStandardItem(str(book["book_id"])),  # скрытая колонка с id
        ]
        self.order_model.appendRow(row)

    def confirm_order(self):
        if self.order_model.rowCount() == 0:
            QMessageBox.warning(self, "Ошибка", "Добавьте книги в заказ")
            return

        books = []
        total = 0

        for i in range(self.order_model.rowCount()):
            price = float(self.order_model.item(i, 2).text())
            total += price
            books.append({
                "book_id": self.order_model.item(i, 3).text()
            })

        dao.create_order(books, self.user_id, total)
        QMessageBox.information(self, "Готово", f"Заказ оформлен\nСумма: {total} руб.")
        self.order_model.removeRows(0, self.order_model.rowCount())
        self.load_client_orders()

    def search(self):
        author = self.ui.comboBox_2.currentText()
        if author == "Все":
            self.books = dao.get_all_books()
        else:
            self.books = dao.search_books_by_author(author)

        self.clear_cards()
        self.insert_card(self.books)

    def clear_cards(self):
        while self.ui.verticalLayout_4.count():
            widget = self.ui.verticalLayout_4.takeAt(0).widget()
            widget.setParent(None)

    def load_client_orders(self):
        model = QStandardItemModel()

        model.setHorizontalHeaderLabels(["order_id", "total_sum", "order_date", "order_status"])
        for order in self.my_orders:
            row = [
                QStandardItem(str(order["order_id"])),
                QStandardItem(str(order["total_sum"])),
                QStandardItem(str(order["order_date"])),
                QStandardItem(str(order["order_status"])),
            ]

            model.appendRow(row)

        self.ui.tableView_orders.setModel(model)
        self.ui.tableView_orders.resizeRowsToContents()

    def filter_status(self):
        status = self.ui.comboBox_status.currentText()
        if status == "Все":
            self.show_orders(self.my_orders)
        else:
            filtered = [order for order in self.my_orders if order["order_status"] == status ]
            self.show_orders(filtered)

    def show_orders(self, orders):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["order_id", "total_sum", "order_date", "order_status"])

        for order in orders:
            row = [
                QStandardItem(str(order["order_id"])),
                QStandardItem(str(order["total_sum"])),
                QStandardItem(str(order["order_date"])),
                QStandardItem(str(order["order_status"])),
            ]
            model.appendRow(row)

        self.ui.tableView_orders.setModel(model)
        self.ui.tableView_orders.resizeColumnsToContents()