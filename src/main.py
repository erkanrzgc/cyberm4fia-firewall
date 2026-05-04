import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from src.gui import FirewallGUI
from src.styles import STYLESHEET

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    app = QApplication(sys.argv)

    icon_path = os.path.join(PROJECT_ROOT, "assets", "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    app.setStyleSheet(STYLESHEET)

    gui = FirewallGUI()
    screen = app.primaryScreen()
    screen_size = screen.size()
    gui.resize(int(screen_size.width() * 0.6), int(screen_size.height() * 0.6))

    if os.path.exists(icon_path):
        gui.setWindowIcon(QIcon(icon_path))

    gui.show()
    sys.exit(app.exec_())
