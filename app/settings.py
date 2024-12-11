from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QToolButton,
    QVBoxLayout,
)

from app.config_file import ConfigFile
from app.icons import get_icon


class Settings:
    """Settings for the application. These are saved to disk and loaded on startup."""

    def __init__(self, alias_file: str = ""):
        self.alias_file = alias_file
        self.source = ConfigFile("settings.json")

    def set_alias_file(self, alias_file: str):
        """Sets the path to the alias file."""
        self.alias_file = alias_file
        self.save()

    def load(self):
        """Loads the settings from disk."""
        self._from_json(self.source.load())

    def save(self):
        """Saves the settings to disk."""
        self.source.save(self._to_json())

    def _to_json(self):
        return {
            "alias_file": self.alias_file,
        }

    def _from_json(self, data: dict):
        if "alias_file" in data:
            self.alias_file = data["alias_file"]


class SettingsDialog(QDialog):
    """Dialog to change application settings."""

    def __init__(self, settings: Settings):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self.alias_file_edit = QLineEdit(settings.alias_file)
        self.alias_file_edit.setReadOnly(True)
        select_alias_file_button = QToolButton()
        select_alias_file_button.setIcon(get_icon("folder.png"))

        alias_file_layout = QHBoxLayout()
        alias_file_layout.addWidget(QLabel("Alias File"))
        alias_file_layout.addWidget(self.alias_file_edit)
        alias_file_layout.addWidget(select_alias_file_button)

        buttons = QDialogButtonBox()
        buttons.addButton(QDialogButtonBox.StandardButton.Save)
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(alias_file_layout)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def to_settings(self) -> Settings:
        return Settings(alias_file=self.alias_file_edit.text())
