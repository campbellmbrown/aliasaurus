from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout

from app.version import GIT_SHA, __version__


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aliasaurus")
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Version: {__version__}"))
        layout.addWidget(QLabel(f"SHA: {GIT_SHA}"))
        layout.addWidget(QLabel("Author: Campbell Brown"))
        github_label = QLabel(
            'GitHub: <a href="https://github.com/campbellmbrown/aliasaurus">campbellmbrown/aliasaurus</a>'
        )
        github_label.setOpenExternalLinks(True)
        layout.addWidget(github_label)
        self.setLayout(layout)
