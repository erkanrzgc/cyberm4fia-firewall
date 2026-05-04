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
    print("ERROR: CyberM4fia Firewall requires root privileges on Linux!")
    print("Usage: sudo python3 firewall.py")
    sys.exit(1)

from src.main import main

if __name__ == "__main__":
    main()
