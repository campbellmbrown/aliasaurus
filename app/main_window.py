import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QSplitter,
    QToolBar,
)

from app.about_dialog import AboutDialog
from app.alias_edit import AliasEdit
from app.alias_file import AliasFile
from app.alias_list import AliasList


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aliasaurus")
        self.resize(600, 400)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

        self.alias_file = AliasFile()
        self.aliases = self.alias_file.decode()

        self.alias_edit = AliasEdit()
        self.alias_edit.unsaved_changes.connect(self._on_unsaved_changes)

        self.save_action = QAction("&Save", self)
        self.save_action.triggered.connect(self._on_save)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setEnabled(False)
        self.revert_action = QAction("&Revert", self)
        self.revert_action.triggered.connect(self._on_revert)
        self.revert_action.setShortcut("Ctrl+Z")
        self.revert_action.setEnabled(False)
        self.delete_action = QAction("&Delete", self)
        self.delete_action.triggered.connect(self._on_delete)
        self.delete_action.setShortcut("Delete")
        self.delete_action.setEnabled(False)
        self.new_action = QAction("&New", self)
        self.new_action.triggered.connect(self._on_new)
        self.new_action.setShortcut("Ctrl+N")

        file_menu = QMenu("&File", self)
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.revert_action)
        file_menu.addAction(self.delete_action)
        file_menu.addSeparator()
        file_menu.addAction("Create &Backup", self.alias_file.backup)
        file_menu.addAction("&Open Alias Directory", self.alias_file.open)
        file_menu.addSeparator()
        file_menu.addAction("&Exit", self.close)

        help_menu = QMenu("&Help", self)
        help_menu.addAction("&About", self._show_about)

        menu_bar = QMenuBar()
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(help_menu)
        self.setMenuBar(menu_bar)

        tool_bar = QToolBar()
        tool_bar.addAction(self.new_action)
        tool_bar.addAction(self.save_action)
        tool_bar.addAction(self.revert_action)
        tool_bar.addAction(self.delete_action)
        self.addToolBar(tool_bar)

        context_menu = QMenu(self)
        context_menu.addAction(self.new_action)
        context_menu.addAction(self.delete_action)

        self.alias_list = AliasList(context_menu)
        self.alias_list.alias_selected.connect(self._on_alias_selected)
        self.alias_list.populate(list(self.aliases.keys()))

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: #d3d3d3; }")
        splitter.addWidget(self.alias_list)
        splitter.addWidget(self.alias_edit)
        splitter.setSizes([200, 400])

        self.setCentralWidget(splitter)

    def _show_about(self):
        """Show the about dialog."""
        about_dialog = AboutDialog()
        about_dialog.exec_()

    def _on_alias_selected(self, name: str):
        something_selected = bool(name)
        self.delete_action.setEnabled(something_selected)
        if something_selected:
            assert name in self.aliases
            self.alias_edit.set(name, self.aliases[name])
        else:
            self.alias_edit.clear()

    def _on_unsaved_changes(self, unsaved: bool):
        """Update the save and revert actions based on unsaved changes."""
        self.save_action.setEnabled(unsaved)
        self.revert_action.setEnabled(unsaved)

    def _on_save(self):
        """Save the current alias."""
        old_name, new_name, commands = self.alias_edit.get()
        if new_name != old_name:
            # Make sure we haven't changed the alias name to something that already exists
            if new_name in self.aliases:
                QMessageBox.warning(self, "Duplicate Alias", "An alias with this name already exists.")
                return
            self.alias_list.update(old_name, new_name)
            self.aliases.pop(old_name)
        self.alias_edit.set(new_name, commands)
        self.aliases[new_name] = commands
        self.alias_file.encode(self.aliases)

    def _on_revert(self):
        """Revert the current alias."""
        self.alias_edit.revert()

    def _on_delete(self):
        """Delete the current alias."""
        selected_alias, _, _ = self.alias_edit.get()
        reply = QMessageBox.question(
            self, "Delete Alias", f"Are you sure you want to delete the alias '{selected_alias}'?"
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.aliases.pop(selected_alias)
            self.alias_list.remove(selected_alias)
            self.alias_file.encode(self.aliases)

    def _on_new(self):
        """Create a new alias."""
        suffix = 1
        while f"alias{suffix}" in self.aliases:
            suffix += 1
        new_alias = f"alias{suffix}"
        self.aliases[new_alias] = ["echo Implement me!"]
        self.alias_list.add(new_alias)
        self.alias_file.encode(self.aliases)
