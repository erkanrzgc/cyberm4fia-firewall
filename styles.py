STYLESHEET = """
QWidget {
     background-color: #121212;
     color: #E0E0E0;
     font-size: 14px;
     font-family: "JetBrains Mono", "Monospace", "Courier New", monospace;
}
QPushButton {
     background-color: rgba(1, 50, 32, 0.6);
     border: none;
     padding: 12px;
     border-radius: 8px;
     font-size: 14px;
     font-weight: bold;
     color: #E0E0E0;
     transition: 0.2s;
}
QPushButton:hover {
     background-color: rgba(1, 80, 50, 0.7);
}
QPushButton:pressed {
     background-color: rgba(1, 30, 20, 0.8);
}
QLineEdit, QTextEdit, QListWidget, QTableWidget {
     background-color: rgba(40, 40, 40, 0.7);
     border: 1px solid #555;
     color: #E0E0E0;
     selection-background-color: rgba(1, 50, 32, 0.5);
     border-radius: 6px;
     padding: 6px;
     font-size: 14px;
}
QLabel {
     font-size: 15px;
     font-weight: bold;
     color: rgba(1, 120, 70, 0.8);
}
QHeaderView::section {
     background-color: #1E1E1E;
     padding: 6px;
     border: 1px solid #333;
     font-weight: bold;
     color: #D0D0D0;
     font-size: 13px;
}
QTableWidget {
    gridline-color: #333;
}
QTableWidget::item {
    padding-top: 8px;
    padding-bottom: 8px;
}
"""
