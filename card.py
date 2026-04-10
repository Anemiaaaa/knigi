from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from db import dao
from gen.card import Ui_Card_Form


class CardWindow(QWidget):
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

        authors = dao.get_all_authors()
        self.ui.comboBox.addItems(author["author"] for author in authors)
        self.ui.comboBox.setCurrentText(self.book["author"])

        image_path = "C:\\Users\\amiri\\PycharmProjects\\knigi\\image\\" + self.book["image"] + ".png"
        pixmap = QPixmap(image_path).scaled(100, 100)
        self.ui.label_image.setPixmap(pixmap)

    def mousePressEvent(self, event: QMouseEvent):
        self.clicked.emit(self.book)
        super().mousePressEvent(event)
