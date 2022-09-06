from decimal import Decimal
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget
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

        default_entry1 = EntryWidget()
        default_entry2 = EntryWidget()

        self.ppp_entry_list = [default_entry1, default_entry2]

        for entry in self.ppp_entry_list:
            entry.amountEdited.connect(self.entry_changed)
            entry.currencyChanged.connect(self.entry_changed)
            self.layout.addWidget(entry)

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
        layout = QHBoxLayout(self)
        layout.addWidget(EntryList(self))
