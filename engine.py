import logging
import os
import socket as _socket
import sys as _sys

from PyQt5.QtCore import QThread, pyqtSignal

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "firewall_logs.txt")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_to_file(message, level="info"):
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)


PROTOCOL_MAP = {
    1: "ICMP",
    2: "IGMP",
    6: "TCP",
    8: "EGP",
    9: "IGP",
    17: "UDP",
    41: "IPv6",
    50: "ESP (Encapsulation Security Payload)",
    51: "AH (Authentication Header)",
    58: "ICMPv6",
    89: "OSPF (Open Shortest Path First)",
    112: "VRRP (Virtual Router Redundancy Protocol)",
    132: "SCTP (Stream Control Transmission Protocol)",
    137: "MPLS-in-IP",
    143: "EtherIP",
    255: "Experimental (Reserved)"
}


def get_protocol_name(protocol):
    if isinstance(protocol, tuple):
        protocol = protocol[0]
    return PROTOCOL_MAP.get(protocol, f"Unknown ({protocol})")


class BaseEngine(QThread):
    log_signal = pyqtSignal(str, str, str)
    rules_signal = pyqtSignal(str)

    def __init__(self, rules, website_filter, parent=None):
        super().__init__(parent)
        self.rules = rules
        self.website_filter = website_filter
        self.running = True

    def resolve_url_to_ip(self, url):
        try:
            _socket.setdefaulttimeout(2)
            return _socket.gethostbyname(url)
        except (_socket.gaierror, _socket.timeout):
            return None

    def run(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError


def create_engine(rules, website_filter, parent=None):
    if _sys.platform == "win32":
        from engine_windows import WindowsEngine
        return WindowsEngine(rules, website_filter, parent)
    else:
        from engine_linux import LinuxEngine
        return LinuxEngine(rules, website_filter, parent)
