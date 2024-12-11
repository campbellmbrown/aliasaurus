from PyQt5.QtCore import Qt, pyqtSignal
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
        self.itemSelectionChanged.connect(self._on_item_selected)
        self.setFont(QFont("Consolas"))

    def add_row(self, name: str):
        """Add a new row to the list.

        Args:
            name (str): The name of the alias to add.
        """
        self.insertItem(self.count(), name)

    def update(self, old_name: str, new_name: str):
        """Update the name of an alias in the list.

        Args:
            old_name (str): The current name of the alias.
            new_name (str): The new name of the alias.
        """
        items = self.findItems(old_name, Qt.MatchFlag.MatchExactly)
        assert len(items) == 1
        items[0].setText(new_name)

    def _on_item_selected(self):
        item = self.currentItem()
        selected = item.text() if item is not None else ""
        self.alias_selected.emit(selected)

    def contextMenuEvent(self, event: QContextMenuEvent):
        self.menu.exec_(event.globalPos())
