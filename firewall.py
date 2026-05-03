#!/usr/bin/env python3
import locale
import os
import socket
import sys

try:
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, "C.UTF-8")
    except locale.Error:
        pass

socket.setdefaulttimeout(2)

if sys.platform != "win32" and os.geteuid() != 0:
    print("ERROR: Firewall must be run as root (sudo) on Linux!")
    print("Usage: sudo python3 firewall.py")
    sys.exit(1)

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from gui import FirewallGUI
from styles import STYLESHEET


def main():
    app = QApplication(sys.argv)

    icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
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


if __name__ == "__main__":
    main()
