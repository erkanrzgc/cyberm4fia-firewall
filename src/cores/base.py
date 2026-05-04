import socket as _socket

from PyQt5.QtCore import QThread, pyqtSignal


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
