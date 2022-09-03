import base64
from typing import List
from typing_extensions import Self
from PySide6.QtWidgets import (
    QWidget,
    QDoubleSpinBox,
    QComboBox,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtGui import QIcon, QPixmap
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

        self.amount = QDoubleSpinBox(self)
        self.amount.setObjectName("valueInput")
        self.amount.setButtonSymbols(QDoubleSpinBox.NoButtons)

        self.selector = QComboBox(self)
        self.selector.setObjectName("chooser")

        self.add_countries(self.selector)
        self.selector.setMaxVisibleItems(15)

        sp = QSizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Maximum)
        self.selector.setSizePolicy(sp)

        layout.addWidget(self.selector)
        layout.addWidget(self.amount)

    def add_countries(self: Self, selector: QComboBox) -> None:
        countries = get_pppdata()
        for country_name, data in countries.items():
            image_blob = base64.b64decode(data["flag"])
            image = QPixmap()
            image.loadFromData(image_blob)
            icon = QIcon(image)
            selector.addItem(
                icon,
                "{name} - {currency}".format(
                    name=country_name, currency=data["currency"]["name"]
                ),
            )
