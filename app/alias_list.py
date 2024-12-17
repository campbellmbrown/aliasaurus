from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QContextMenuEvent, QFont, QKeyEvent
from PyQt5.QtWidgets import QListView, QListWidget, QMenu


class AliasList(QListWidget):
    """A list of aliases that can be rearranged."""

    alias_selected = pyqtSignal(str)
    order_changed = pyqtSignal()

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

    def populate(self, names: list[str]):
        """Populate the list with aliases.

        Args:
            names (list[str]): A list of alias names.
        """
        self.addItems(names)

    def add(self, name: str):
        """Add a new alias to the list.

        Args:
            name (str): The name of the alias to add.
        """
        self.insertItem(self.count(), name)
        self.setCurrentRow(self.count() - 1)

    def remove(self, name: str):
        """Remove an alias from the list.

        Args:
            name (str): The name of the alias to remove.
        """
        items = self.findItems(name, Qt.MatchFlag.MatchExactly)
        assert len(items) == 1
        self.takeItem(self.row(items[0]))

    def update(self, old_name: str, new_name: str):
        """Update the name of an alias in the list.

        Args:
            old_name (str): The current name of the alias.
            new_name (str): The new name of the alias.
        """
        items = self.findItems(old_name, Qt.MatchFlag.MatchExactly)
        assert len(items) == 1
        items[0].setText(new_name)

    def get_all_in_order(self) -> list[str]:
        """Get all the aliases in the list in order.

        Returns:
            list[str]: A list of alias names.
        """
        items = [self.item(i) for i in range(self.count())]
        return [item.text() for item in items if item is not None]

    def _on_item_selected(self):
        item = self.currentItem()
        selected = item.text() if item is not None else ""
        self.alias_selected.emit(selected)

    def contextMenuEvent(self, event: QContextMenuEvent):
        self.menu.exec_(event.globalPos())

    def dropEvent(self, event):
        super().dropEvent(event)
        self.order_changed.emit()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.setCurrentItem(None)
        else:
            super().keyPressEvent(event)
