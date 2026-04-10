import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from auth import AuthWindow
import sys

if __name__ == "__main__":

    app = QApplication(sys.argv)

    if os.path.isfile("icon.png"):
        app.setWindowIcon(QIcon("icon.png"))

    window = AuthWindow()
    window.show()

    sys.exit(app.exec())

