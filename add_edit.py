from PyQt6.QtWidgets import QDialog, QFileDialog

from gen.add_edit_dialog import Ui_Dialog


class AddEditWindow(QDialog):
    def __init__(self, book :dict | None = None):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.book = book
        self.__conn()

    def __conn(self):
        self.ui.pushButton_add_image.clicked.connect(self.add_image)
        self.ui.pushButton_save.clicked.connect(self.accept)

    def get(self):
        author = self.ui.authorLineEdit.text()
        book_name = self.ui.book_nameLineEdit.text()
        price = self.ui.priceDoubleSpinBox.value()
        discount = self.ui.discountDoubleSpinBox.value()
        image = self.ui.imageLineEdit.text()

        return author, book_name, price, discount, image

    def load(self):
        self.ui.authorLineEdit.setText(self.book["author"])
        self.ui.book_nameLineEdit.setText(self.book["book_name"])
        self.ui.priceDoubleSpinBox.setValue(float(self.book["price"]))
        self.ui.discountDoubleSpinBox.setValue(float(self.book["discount"]))
        self.ui.imageLineEdit.setText(self.book["image"])

    def add_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите фото", "image/", "All Files (*)")
        if path:
            self.ui.imageLineEdit.setText(path)
