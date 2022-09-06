import sys

from PySide6.QtWidgets import (
    QApplication,
    QGraphicsDropShadowEffect,
    QVBoxLayout,
    QWidget,
)

import rc_icons  # icons: don't remove
from conf import CSS_FILE
from pages.home import HomePage


class Convert(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(320, 124)
        # remove default title bar
        self.setWindowTitle("PPP calculator")
        self.resize(420, self.height())
        self.setAutoFillBackground(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("main")
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.home = HomePage(self)
        main_layout.addWidget(self.home)

        self.setLayout(main_layout)


app = QApplication(sys.argv)
app.setStyle("Fusion")
app.setStyleSheet(CSS_FILE.read_text())
window = Convert()
sys.exit(app.exec())
