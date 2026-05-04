import os
import socket
from urllib.parse import urlparse

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.cores import create_engine

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FirewallGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberM4fia Firewall")

        icon_path = os.path.join(PROJECT_ROOT, "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.resize(screen_size.width() // 2, screen_size.height() // 2)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout()

        self.start_button = QPushButton("Start Firewall")
        self.start_button.clicked.connect(self.start_firewall)
        self.stop_button = QPushButton("Stop Firewall")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_firewall)

        rule_layout = QHBoxLayout()
        self.rule_label = QLabel("Rules:")
        self.rule_list = QListWidget()
        self.rule_input = QLineEdit()
        self.rule_input.setPlaceholderText(
            "Enter rule: tcp, udp, :80, 192.168.1.1:443"
        )
        self.add_rule_button = QPushButton("Add Rule")
        self.add_rule_button.clicked.connect(self.add_rule)
        rule_layout.addWidget(self.rule_input)
        rule_layout.addWidget(self.add_rule_button)
        self.delete_rule_button = QPushButton("Delete Selected Rule")
        self.delete_rule_button.clicked.connect(self.delete_rule)

        self.network_label = QLabel("Network Traffic:")
        self.log_area = QTableWidget()
        self.log_area.setColumnCount(3)
        self.log_area.setHorizontalHeaderLabels(["Source", "Destination", "Protocol"])
        self.log_area.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.log_area.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.rules_label = QLabel("Applied Rules:")
        self.rules_area = QTextEdit()
        self.rules_area.setReadOnly(True)

        self.web_label = QLabel("Blocked Websites:")
        self.web_list = QListWidget()

        website_layout = QHBoxLayout()
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("Enter website to block: www.example.com")
        self.add_website_button = QPushButton("Add Website")
        self.add_website_button.clicked.connect(self.add_website)
        website_layout.addWidget(self.website_input)
        website_layout.addWidget(self.add_website_button)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.rule_label)
        layout.addWidget(self.rule_list)
        layout.addLayout(rule_layout)
        layout.addWidget(self.delete_rule_button)
        layout.addWidget(self.network_label)
        layout.addWidget(self.log_area)
        layout.addWidget(self.rules_label)
        layout.addWidget(self.rules_area)
        layout.addWidget(self.web_label)
        layout.addWidget(self.web_list)
        layout.addLayout(website_layout)
        self.main_widget.setLayout(layout)

        self.firewall_worker = None
        self.rules = []
        self.website_filter = set()

    @pyqtSlot(str, str, str)
    def add_to_traffic_table(self, src, dst, protocol):
        row_position = self.log_area.rowCount()
        self.log_area.insertRow(row_position)
        self.log_area.setItem(row_position, 0, QTableWidgetItem(src))
        self.log_area.setItem(row_position, 1, QTableWidgetItem(dst))
        self.log_area.setItem(row_position, 2, QTableWidgetItem(protocol))

    def add_rule(self):
        raw_rule = self.rule_input.text().strip()
        if not raw_rule:
            QMessageBox.warning(self, "Warning", "Enter a valid rule!")
            return

        if raw_rule.isdigit():
            rule = f":{raw_rule}"
        else:
            rule = raw_rule.lower()

        if rule not in self.rules:
            self.rules.append(rule)
            self.rule_list.addItem(rule)
            self.rules_area.append(f"Rule Added: {rule}")
            self.rule_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Rule already exists!")

    def delete_rule(self):
        selected_item = self.rule_list.currentItem()
        if selected_item:
            rule = selected_item.text()
            if rule in self.rules:
                self.rules.remove(rule)
            self.rule_list.takeItem(self.rule_list.row(selected_item))
            self.rules_area.append(f"Rule Deleted: {rule}")
        else:
            QMessageBox.warning(self, "Warning", "Select a Rule to Delete!")

    def start_firewall(self):
        if not self.firewall_worker:
            self.firewall_worker = create_engine(self.rules, self.website_filter)
            self.firewall_worker.log_signal.connect(self.add_to_traffic_table)
            self.firewall_worker.rules_signal.connect(self.rules_area.append)
            self.firewall_worker.start()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.rules_area.append("Firewall Started")

    def add_website(self):
        raw_input = self.website_input.text().strip()
        if not raw_input:
            QMessageBox.warning(self, "Warning", "Enter a Valid URL!")
            return

        try:
            parsed = urlparse(raw_input if "://" in raw_input else "http://" + raw_input)
            domain = parsed.netloc
            if not domain:
                raise ValueError("No domain found")
        except Exception:
            QMessageBox.critical(self, "Error", "Invalid URL format!")
            return

        ip = None
        if self.firewall_worker:
            ip = self.firewall_worker.resolve_url_to_ip(domain)
        else:
            try:
                socket.setdefaulttimeout(2)
                ip = socket.gethostbyname(domain)
            except Exception:
                ip = None

        if ip:
            self.website_filter.add(ip)
            self.web_list.addItem(f"{domain} ({ip})")
            self.website_input.clear()
            self.rules_area.append(f"Added to Website Filter: {domain} ({ip})")
        else:
            QMessageBox.critical(self, "Error", "Unable to resolve domain to IP!")

    def stop_firewall(self):
        if self.firewall_worker:
            self.firewall_worker.stop()
            self.firewall_worker = None
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.rules_area.append("Firewall Stopped")
