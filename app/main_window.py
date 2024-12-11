from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QMainWindow, QMenu, QMenuBar, QSplitter

from app.icons import get_icon
from app.settings import Settings, SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aliasaurus")
        self.resize(600, 400)

        self.settings = Settings()
        self.settings.load()

        file_menu = QMenu("&File", self)
        file_menu.addAction(get_icon("gear.png"), "&Settings", self._on_open_settings)
        file_menu.addSeparator()
        file_menu.addAction(get_icon("x.png"), "&Exit", self.close)

        menu_bar = QMenuBar()
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: #d3d3d3; }")
        splitter.addWidget(QLabel("Left"))
        splitter.addWidget(QLabel("Right"))
        splitter.setSizes([200, 400])

        self.setCentralWidget(splitter)

    def _on_open_settings(self):
        """Show the settings dialog."""
        settings_dialog = SettingsDialog(self.settings)
        result = settings_dialog.exec_()
        if result == QDialog.DialogCode.Accepted:
            self.settings = settings_dialog.to_settings()
            self.settings.save()
