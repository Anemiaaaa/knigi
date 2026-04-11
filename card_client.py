from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap, QMouseEvent
from PyQt6.QtWidgets import QWidget, QMessageBox

from db import dao
from gen.card_client import Ui_Card_Form


class ClientCardWindow(QWidget):
    clicked = pyqtSignal(dict)
    def __init__(self, book):
        super().__init__()
        self.ui = Ui_Card_Form()
        self.ui.setupUi(self)
        self.book = book
        self.insert_card()

    def insert_card(self):
        self.ui.label_name.setText(self.book["book_name"])
        self.ui.label_price.setText(str(self.book["price"]))
        self.ui.label_author.setText(self.book["author"])

        image_path = "C:\\Users\\amiri\\PycharmProjects\\knigi\\image\\" + self.book["image"] + ".png"
        pixmap = QPixmap(image_path).scaled(100, 100)
        self.ui.label_image.setPixmap(pixmap)

    def mousePressEvent(self, event: QMouseEvent):
        self.clicked.emit(self.book)
        super().mousePressEvent(event)
        QMessageBox.information(self, "Инфо", "Книга добавлена в заказ")