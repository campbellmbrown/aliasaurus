import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QMainWindow, QMenu, QMenuBar, QSplitter

from app.about_dialog import AboutDialog
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

        file_menu = QMenu("&File", self)
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

        self.alias_list = AliasList()
        for alias in self.aliases.keys():
            self.alias_list.add_row(alias)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: #d3d3d3; }")
        splitter.addWidget(self.alias_list)
        splitter.addWidget(QLabel("Right"))
        splitter.setSizes([200, 400])

        self.setCentralWidget(splitter)

    def _show_about(self):
        """Show the about dialog."""
        about_dialog = AboutDialog()
        about_dialog.exec_()
