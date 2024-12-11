from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListView, QListWidget


class AliasList(QListWidget):
    """A list of aliases that can be rearranged."""

    alias_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QListView.DragDropMode.InternalMove)
        self.setDropIndicatorShown(True)
        self.setAlternatingRowColors(True)
        self.setFont(QFont("Consolas"))

    def add_row(self, text: str):
        self.insertItem(self.count(), text)
