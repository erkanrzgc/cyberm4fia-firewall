STYLESHEET = """
QWidget {
     background-color: #0D1117;
     color: #C9D1D9;
     font-size: 14px;
     font-family: "JetBrains Mono", "Monospace", "Courier New", monospace;
}
QPushButton {
     background-color: rgba(1, 50, 32, 0.7);
     border: 1px solid rgba(0, 255, 100, 0.15);
     padding: 12px 24px;
     border-radius: 6px;
     font-size: 14px;
     font-weight: bold;
     color: #C9D1D9;
}
QPushButton:hover {
     background-color: rgba(0, 160, 80, 0.25);
     border: 1px solid rgba(0, 255, 100, 0.4);
}
QPushButton:pressed {
     background-color: rgba(1, 30, 20, 0.9);
}
QPushButton:disabled {
     background-color: rgba(40, 40, 40, 0.5);
     color: #555;
     border: 1px solid #333;
}
QLineEdit {
     background-color: rgba(22, 27, 34, 0.8);
     border: 1px solid #30363D;
     color: #C9D1D9;
     placeholder-text-color: #8B949E;
     selection-background-color: rgba(1, 80, 50, 0.5);
     border-radius: 6px;
     padding: 6px;
     font-size: 14px;
}
QTextEdit, QListWidget, QTableWidget {
     background-color: rgba(22, 27, 34, 0.8);
     border: 1px solid #30363D;
     color: #C9D1D9;
     selection-background-color: rgba(1, 80, 50, 0.5);
     border-radius: 6px;
     padding: 6px;
     font-size: 14px;
}
QLabel {
     font-size: 15px;
     font-weight: bold;
     color: #58A6FF;
     padding: 4px 0;
}
QHeaderView::section {
     background-color: #161B22;
     padding: 6px;
     border: 1px solid #30363D;
     font-weight: bold;
     color: #8B949E;
     font-size: 13px;
}
QTableWidget {
    gridline-color: #21262D;
}
QTableWidget::item {
    padding-top: 8px;
    padding-bottom: 8px;
}
QListWidget::item:selected {
    background-color: rgba(1, 80, 50, 0.4);
}
QTextEdit {
    background-color: rgba(13, 17, 23, 0.9);
}
"""
