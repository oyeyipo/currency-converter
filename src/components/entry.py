from email.policy import default
from PySide6.QtWidgets import QWidget, QLineEdit, QComboBox, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QSize
from utilities.loader import get_pppdata

HIEGHT = 45


class EntryWidget(QWidget):
    def __init__(self, parent=None, defaults: dict = {}) -> None:
        super().__init__(parent)
        self.defaults = defaults.copy()

        self.setObjectName("entryComponent")
        self.initializeUI()

    def initializeUI(self):

        layout = QHBoxLayout(self)

        self.amount = QLineEdit(self)
        self.amount.setObjectName("valueInput")
        self.amount.setValidator(QIntValidator(self))
        self.amount.setText(self.defaults.get("prev_value", ""))
        self.amount.setPlaceholderText("0")
        # self.amount.textChanged.connect(self.calculatePPP)

        self.selector = QComboBox(self)
        self.selector.setObjectName("chooser")

        self.ppp_data = get_pppdata()

        self.selector.addItems(self.ppp_data.keys())
        self.selector.setMaxVisibleItems(10)
        sp = QSizePolicy()
        sp.setHorizontalStretch(0)
        sp.setHorizontalPolicy(QSizePolicy.Minimum)
        self.selector.setSizePolicy(sp)
        # self.selector.currentTextChanged.connect()

        layout.addWidget(self.selector)
        layout.addWidget(self.amount)
