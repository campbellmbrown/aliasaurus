from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QContextMenuEvent, QFont
from PyQt5.QtWidgets import QListView, QListWidget, QMenu


class AliasList(QListWidget):
    """A list of aliases that can be rearranged."""

    alias_selected = pyqtSignal(str)

    def __init__(self, menu: QMenu, parent=None):
        super().__init__(parent)
        self.menu = menu
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QListView.DragDropMode.InternalMove)
        self.setDropIndicatorShown(True)
        self.setAlternatingRowColors(True)
        self.setFont(QFont("Consolas"))

    def add_row(self, text: str):
        self.insertItem(self.count(), text)

    def contextMenuEvent(self, event: QContextMenuEvent):
        self.menu.exec_(event.globalPos())
