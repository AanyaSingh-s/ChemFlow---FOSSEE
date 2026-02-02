# desktop/main.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow
def main():
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    
    # Set global stylesheet matching website design system
    # Colors from src/index.css (dark theme)
    # Primary: #3b82f6 (blue)
    # Background: #0f172a (dark navy)
    # Card: #1a2a47 (dark slate)
    # Foreground: #f1f5f9 (light)
    # Muted: #64748b (gray)
    # Border: #334155 (dark gray)
    
    app.setStyleSheet("""
        * {
            font-family: -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            font-size: 11px;
        }
        
        QMainWindow {
            background: #0f172a;
        }
        
        QWidget {
            color: #f1f5f9;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3b82f6,
                stop:1 #2563eb);
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 11px;
            outline: none;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2563eb,
                stop:1 #1d4ed8);
        }
        
        QPushButton:pressed {
            background: #1e40af;
        }
        
        QPushButton:disabled {
            background: #475569;
            color: #94a3b8;
        }
        
        QLineEdit {
            background: #1e293b;
            border: 2px solid #334155;
            border-radius: 6px;
            padding: 8px 12px;
            color: #f1f5f9;
            font-size: 11px;
            selection-background-color: #3b82f6;
        }
        
        QLineEdit:focus {
            border: 2px solid #3b82f6;
            background: #1a2a47;
        }
        
        QLineEdit::placeholder {
            color: #64748b;
        }
        
        QLabel {
            color: #f1f5f9;
            font-size: 11px;
        }
        
        QTabWidget::pane {
            border: none;
            background: transparent;
        }
        
        QTabBar {
            background: transparent;
            border: none;
        }
        
        QTabBar::tab {
            background: transparent;
            color: #64748b;
            border: none;
            border-bottom: 3px solid transparent;
            padding: 8px 16px;
            margin-right: 0px;
            font-weight: 600;
            font-size: 12px;
        }
        
        QTabBar::tab:selected {
            color: #ffffff;
            border-bottom: 3px solid #3b82f6;
        }
        
        QTabBar::tab:hover {
            color: #cbd5e1;
        }
        
        QTableWidget {
            background: #1a2a47;
            border: 1px solid #334155;
            border-radius: 6px;
            gridline-color: rgba(51, 65, 85, 0.3);
            color: #f1f5f9;
        }
        
        QTableWidget::item {
            padding: 8px 12px;
            border: none;
        }
        
        QTableWidget::item:selected {
            background: rgba(59, 130, 246, 0.2);
            color: #ffffff;
        }
        
        QHeaderView::section {
            background: #0f172a;
            color: #cbd5e1;
            border: none;
            border-right: 1px solid #334155;
            border-bottom: 1px solid #334155;
            padding: 8px 12px;
            font-weight: 600;
            font-size: 12px;
        }
        
        QScrollBar:vertical {
            background: #0f172a;
            width: 10px;
            border-radius: 5px;
            margin: 0px 0px 0px 0px;
        }
        
        QScrollBar::handle:vertical {
            background: #334155;
            border-radius: 5px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #475569;
        }
        
        QScrollBar:horizontal {
            background: #0f172a;
            height: 10px;
            border-radius: 5px;
            margin: 0px 0px 0px 0px;
        }
        
        QScrollBar::handle:horizontal {
            background: #334155;
            border-radius: 5px;
            min-width: 30px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #475569;
        }
        
        QScrollBar::add-line, QScrollBar::sub-line {
            border: none;
            background: none;
        }
        
        QMenuBar {
            background: #0f172a;
            color: #f1f5f9;
            border-bottom: 1px solid #334155;
        }
        
        QMenuBar::item {
            padding: 6px 14px;
            background: transparent;
        }
        
        QMenuBar::item:selected {
            background: rgba(59, 130, 246, 0.1);
        }
        
        QMenu {
            background: #1a2a47;
            border: 1px solid #334155;
            border-radius: 6px;
            color: #f1f5f9;
        }
        
        QMenu::item {
            padding: 6px 20px;
        }
        
        QMenu::item:selected {
            background: rgba(59, 130, 246, 0.2);
        }
        
        QStatusBar {
            background: #0f172a;
            color: #cbd5e1;
            border-top: 1px solid #334155;
        }
        
        QDialog {
            background: #0f172a;
        }
        
        QComboBox {
            background: #1e293b;
            border: 2px solid #334155;
            border-radius: 6px;
            padding: 6px 10px;
            color: #f1f5f9;
            font-size: 13px;
        }
        
        QComboBox:hover {
            border: 2px solid #3b82f6;
        }
        
        QComboBox:focus {
            border: 2px solid #3b82f6;
            background: #1a2a47;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox QAbstractItemView {
            background: #1a2a47;
            border: 1px solid #334155;
            border-radius: 6px;
            selection-background-color: rgba(59, 130, 246, 0.2);
            color: #f1f5f9;
        }
        
        QFrame {
            color: #f1f5f9;
        }
        
        QScrollArea {
            background: transparent;
            border: none;
        }
        
        QCheckBox {
            color: #f1f5f9;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border-radius: 3px;
            border: 2px solid #334155;
            background: #1e293b;
        }
        
        QCheckBox::indicator:checked {
            background: #3b82f6;
            border: 2px solid #3b82f6;
        }
        
        QSpinBox, QDoubleSpinBox {
            background: #1e293b;
            border: 2px solid #334155;
            border-radius: 6px;
            padding: 6px 8px;
            color: #f1f5f9;
        }
        
        QSpinBox:focus, QDoubleSpinBox:focus {
            border: 2px solid #3b82f6;
        }
        
        QProgressBar {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 6px;
            text-align: center;
            color: #f1f5f9;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3b82f6,
                stop:1 #2563eb);
            border-radius: 4px;
        }
    """)
    
    # Set application metadata
    app.setApplicationName("Chemical Equipment Analyzer")
    app.setOrganizationName("ChemFlow Analytics")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()