from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout

from app.icons import get_pixmap
from app.version import GIT_SHA, __version__


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aliasaurus")
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        pixmap = get_pixmap("logo_256x256.png")
        # scale down
        pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(QLabel(f"Version: {__version__}"))
        layout.addWidget(QLabel(f"SHA: {GIT_SHA}"))
        layout.addWidget(QLabel("Author: Campbell Brown"))
        github_label = QLabel(
            'GitHub: <a href="https://github.com/campbellmbrown/aliasaurus">campbellmbrown/aliasaurus</a>'
        )
        github_label.setOpenExternalLinks(True)
        layout.addWidget(github_label)
        self.setLayout(layout)
