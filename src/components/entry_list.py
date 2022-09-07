from decimal import Decimal
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from utilities.helper import commalize, decommalize
from utilities.loader import get_pppdata

from components.entry import EntryWidget


class EntryList(QWidget):
    PPP_DATA = get_pppdata()

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

        self.layout = QVBoxLayout(self)

        default_entry1 = self.get_entry_widget()
        default_entry2 = self.get_entry_widget()

        self.ppp_entry_list = [default_entry1, default_entry2]

        for entry in self.ppp_entry_list:
            self.layout.addWidget(entry, 0)

    def get_entry_widget(self) -> EntryWidget:
        entry = EntryWidget()

        sp = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sp.setHeightForWidth(entry.sizePolicy().hasHeightForWidth())
        entry.setSizePolicy(sp)

        entry.amountEdited.connect(self.entry_changed)
        entry.currencyChanged.connect(self.entry_changed)

        return entry

    def add_new_entry(self):
        new_entry = self.get_entry_widget()
        self.layout.addWidget(new_entry)

    def entry_changed(self, amount: str) -> None:
        if amount:
            self.convert(amount)
        else:
            for entry in self.ppp_entry_list:
                if entry is not self.sender():
                    entry.amount.clear()

    def convert(self, amount: str) -> None:
        """PPP formular: sourceAmount / SourcePPP * TargetPPP"""
        # Get source PPP
        source_widget: EntryWidget = self.sender()
        source_country = source_widget.get_country_name()
        source_ppp = str(self.PPP_DATA[source_country]["ppp"])

        # Get targets
        target_widgets: List[EntryWidget] = self.ppp_entry_list.copy()
        target_widgets.remove(source_widget)

        # Get source amount
        source_amount = decommalize(amount)

        # Calculate result
        for target_widget in target_widgets:
            # Get targets PPP
            target_country = target_widget.get_country_name()
            target_ppp = str(self.PPP_DATA[target_country]["ppp"])

            # formula calc
            target_amount = (
                Decimal(source_amount) / Decimal(source_ppp) * Decimal(target_ppp)
            )
            target_amount = commalize(str(target_amount.quantize(Decimal(".01"))))
            target_widget.amount.setText(target_amount)


class ContentContainer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName("contentContainer")
        self.initializeUi()

    def initializeUi(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout(self)

        self.entry_list = EntryList(self)
        entry_list_sp = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        entry_list_sp.setHeightForWidth(
            self.entry_list.sizePolicy().hasHeightForWidth()
        )
        self.entry_list.setSizePolicy(entry_list_sp)

        vbox.addWidget(self.entry_list, alignment=Qt.AlignHCenter)

        self.add_btn = QPushButton("+")
        self.add_btn.setObjectName("addBtn")
        add_btn_sp = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        add_btn_sp.setHeightForWidth(self.add_btn.sizePolicy().hasHeightForWidth())
        self.add_btn.setSizePolicy(add_btn_sp)
        self.add_btn.clicked.connect(self.add_new_entry)

        vbox.addWidget(self.add_btn, 0, alignment=Qt.AlignHCenter)
        vbox.setAlignment(Qt.AlignCenter)

        hbox.addLayout(vbox)

    def add_new_entry(self):
        self.entry_list.add_new_entry()
