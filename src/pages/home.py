from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)
from components.entry_list import ContentContainer


class HomePage(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initializeUI()

    def initializeUI(self):
        self.setObjectName("homePage")
        self.setUpWindow()

    def setUpWindow(self):
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        content = ContentContainer(self)

        self.content_layout.addWidget(content)
