from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)

from PySide6.QtCore import Qt

from components.entry import EntryWidget


class EntryList(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName("entryComponent")
        self.setAutoFillBackground(True)
        self.initializeUI()

    def initializeUI(self):

        sp = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.setMinimumWidth(320)
        self.setMaximumWidth(420)
        self.setSizePolicy(sp)

        layout = QVBoxLayout(self)

        default_entry1 = EntryWidget()
        default_entry2 = EntryWidget()

        self.ppp_entry_list = [default_entry1, default_entry2]

        for entry in self.ppp_entry_list:
            layout.addWidget(entry)


class ContentContainer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QHBoxLayout(self)
        layout.addWidget(EntryList(self))
