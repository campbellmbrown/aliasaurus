import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QMainWindow, QMenu, QMenuBar, QSplitter

from app.alias_file import AliasFile


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aliasaurus")
        self.resize(600, 400)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

        self.alias_file = AliasFile()

        file_menu = QMenu("&File", self)
        file_menu.addAction("Create &Backup", self.alias_file.backup)
        file_menu.addAction("&Open Alias Directory", self.alias_file.open)
        file_menu.addSeparator()
        file_menu.addAction("&Exit", self.close)

        menu_bar = QMenuBar()
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: #d3d3d3; }")
        splitter.addWidget(QLabel("Left"))
        splitter.addWidget(QLabel("Right"))
        splitter.setSizes([200, 400])

        self.setCentralWidget(splitter)
