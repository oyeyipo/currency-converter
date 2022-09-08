from base64 import b64decode

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDoubleValidator, QIcon, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from typing_extensions import Self
from utilities.helper import commalize
from utilities.loader import get_pppdata


class EntryWidget(QWidget):
    amountEdited = Signal(str)
    currencyChanged = Signal(str)

    def __init__(self, parent=None, defaults: dict = {}) -> None:
        super().__init__(parent)
        self.defaults = defaults.copy()

        self.setObjectName("entryComponent")
        self.initializeUI()

    def initializeUI(self):
        layout = QVBoxLayout(self)

        selector_sp = QSizePolicy()
        selector_sp.setHorizontalPolicy(QSizePolicy.Maximum)
        selector_sp.setVerticalPolicy(QSizePolicy.Maximum)
        selector_sp.setHorizontalStretch(0)

        amount_sp = QSizePolicy()
        amount_sp.setVerticalPolicy(QSizePolicy.Maximum)
        amount_sp.setVerticalStretch(0)

        input_form = QHBoxLayout()

        self.currency_symbol = QLabel()
        self.currency_symbol.setObjectName("symbol")

        self.amount = QLineEdit(self)
        self.amount.setObjectName("valueInput")
        self.amount.setPlaceholderText("0")
        validator = QDoubleValidator()
        validator.setDecimals(2)
        self.amount.setValidator(validator)
        self.amount.textEdited.connect(self.amount_changed)

        input_form.addWidget(self.currency_symbol, alignment=Qt.AlignCenter)
        input_form.addWidget(self.amount)

        self.selector = QComboBox(self)
        self.selector.setObjectName("chooser")
        self.selector.setSizePolicy(selector_sp)
        self.selector.setMaxVisibleItems(15)
        self.selector.currentTextChanged.connect(self.selector_text_changed)

        self.set_countries()
        self._set_currency_symbol()

        layout.addLayout(input_form)
        layout.addWidget(self.selector, stretch=0, alignment=Qt.AlignLeft)

    def set_countries(self: Self) -> None:
        self.countries = get_pppdata()
        for country_name, data in self.countries.items():
            image_blob = b64decode(data["flag"])
            icon = QIcon(self.get_image_from_blob(image_blob))
            self.selector.addItem(
                icon,
                "{name} - {currency}".format(
                    name=country_name, currency=data["currency"]["name"]
                ),
            )

    def get_image_from_blob(self: Self, blob: bytes) -> QPixmap:
        image = QPixmap()
        image.loadFromData(blob)
        return image

    def _set_currency_symbol(self):
        country_name = self.get_country_name()
        country_symbol = self.countries[country_name]["currency"]["symbol"]
        if not country_symbol:
            country_symbol = self.countries[country_name]["currency"]["code"]
        self.currency_symbol.setText(country_symbol)

    def selector_text_changed(self, text: str) -> None:
        self._set_currency_symbol()
        self.currencyChanged.emit(self.amount.text())

    def amount_changed(self, text: str) -> None:
        c_amount = commalize(text)
        self.amount.setText(c_amount)
        self.amountEdited.emit(c_amount)

    def get_country_name(self) -> str:
        name, _ = self.selector.currentText().split(" - ")
        return name
