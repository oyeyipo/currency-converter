import sys
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsDropShadowEffect,
    QWidget,
    QVBoxLayout,
)
from conf import CSS_FILE
from pages.home import HomePage


class Convert(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initializeUI()

    def initializeUI(self):
        # remove default title bar
        self.setMinimumSize(320, 124)
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
app.setStyleSheet(CSS_FILE.read_text())
window = Convert()
sys.exit(app.exec())
