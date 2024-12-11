from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QPlainTextEdit, QVBoxLayout, QWidget


class AliasEdit(QWidget):
    """Widget for editing an alias."""

    unsaved_changes = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.selected_alias = ""
        self.selected_alias_commands: list[str] = []

        self.name_edit = QLineEdit()
        self.name_edit.setFont(QFont("Consolas"))
        self.name_edit.textChanged.connect(self._check_unsaved_changes)
        self.name_edit.setEnabled(False)
        self.commands_edit = QPlainTextEdit()
        self.commands_edit.setFont(QFont("Consolas"))
        self.commands_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.commands_edit.textChanged.connect(self._check_unsaved_changes)
        self.commands_edit.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Alias"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Commands"))
        layout.addWidget(self.commands_edit)
        self.setLayout(layout)

    def clear(self):
        """Clear the alias edit fields and disable editing."""
        self.selected_alias = ""
        self.selected_alias_commands = []
        self.name_edit.clear()
        self.commands_edit.clear()
        self.name_edit.setEnabled(False)
        self.commands_edit.setEnabled(False)

    def set(self, name: str, commands: list[str]):
        """
        Set the alias edit fields and enable editing. This will also save a copy of the original alias so it can be
        reverted to later or checked for unsaved changes.
        """
        self.selected_alias = name
        self.selected_alias_commands = commands
        self.name_edit.setText(name)
        self.commands_edit.setPlainText("\n".join(commands))
        self.name_edit.setEnabled(True)
        self.commands_edit.setEnabled(True)

    def get(self) -> tuple[str, str, list[str]]:
        """Get the current alias edit fields.

        Returns:
            tuple[str, str, list[str]]: The original alias name, the new alias name, and the new alias commands.
        """
        return self.selected_alias, self.name_edit.text(), self.commands_edit.toPlainText().split("\n")

    def revert(self):
        """Revert any unsaved changes to the original alias."""
        self.set(self.selected_alias, self.selected_alias_commands)

    def _check_unsaved_changes(self):
        unsaved_changes = self.commands_edit.toPlainText() != "\n".join(self.selected_alias_commands)
        unsaved_changes |= self.name_edit.text() != self.selected_alias
        self.unsaved_changes.emit(unsaved_changes)
