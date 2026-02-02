# desktop/gui/login_dialog.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTabWidget, QWidget,
    QMessageBox, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class LoginDialog(QDialog):
    def __init__(self, api_client, parent=None, start_with_register=False):
        super().__init__(parent)
        self.api_client = api_client
        self.user_data = None
        self.start_with_register = start_with_register

        self.setWindowTitle("ChemFlow Analytics - Login")
        self.setModal(True)
        self.setFixedSize(500, 560)

        # Clean, modern styling
        self.setStyleSheet("""
            QDialog {
                background: #0f172a;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 32, 24, 32)
        layout.setSpacing(20)

        # App Logo/Title
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setSpacing(8)
        
        logo = QLabel("🧪")
        logo.setStyleSheet("font-size: 32px;")
        logo.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo)
        
        self.app_title = QLabel("ChemFlow")
        self.app_title.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        self.app_title.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.app_title)
        
        self.subtitle = QLabel("Chemical Equipment")
        self.subtitle.setStyleSheet("""
            color: #94a3b8;
            font-size: 9px;
        """)
        self.subtitle.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.subtitle)
        
        layout.addWidget(logo_container)

        # Tabs for Login/Register
        self.tabs = QTabWidget()
        from PyQt5.QtWidgets import QSizePolicy

        self.tabs.tabBar().setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )


        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            
            QTabBar::tab {
                background: transparent;
                color: #64748b;
                padding: 8px 20px;
                font-size: 11px;
                font-weight: 600;
                border: none;
                border-bottom: 3px solid transparent;
                min-width: 110px;
            }
            
            QTabBar::tab:selected {
                color: white;
                border-bottom: 3px solid #3b82f6;
            }
            
            QTabBar::tab:hover {
                color: #cbd5e1;
            }
        """)

        # Login Tab
        login_tab = self.create_login_tab()
        self.tabs.addTab(login_tab, "Login")

        # Register Tab
        register_tab = self.create_register_tab()
        self.tabs.addTab(register_tab, "Register")

        layout.addWidget(self.tabs)

        if self.start_with_register:
            self.tabs.setCurrentIndex(1)

        # Skip Button
        skip_btn = QPushButton("Continue without login (Local Mode)")
        skip_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 2px solid #475569;
                border-radius: 8px;
                color: #94a3b8;
                padding: 8px;
                font-size: 8px;
                font-weight: 600;
            }
            QPushButton:hover {
                border-color: #64748b;
                color: #cbd5e1;
                background: rgba(100, 116, 139, 0.1);
            }
        """)
        skip_btn.clicked.connect(self.reject)
        layout.addWidget(skip_btn)
        
        # Apply theme from parent if available
        try:
            parent_theme = getattr(parent, 'theme', None)
            if parent_theme:
                self.apply_theme(parent_theme)
        except Exception:
            pass

    def create_login_tab(self):
        """Create login tab with clear, visible buttons"""
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 16, 0, 16)
        layout.setSpacing(12)

        # Username
        username_label = QLabel("Username")
        username_label.setStyleSheet("""
            color: white;
            font-size: 9px;
            font-weight: 600;
        """)
        layout.addWidget(username_label)

        self.login_username = QLineEdit()
        self.login_username.setObjectName("login-username")
        self.login_username.setPlaceholderText("Enter your username")
        self.login_username.setStyleSheet(self.get_input_style())
        layout.addWidget(self.login_username)

        # Password
        password_label = QLabel("Password")
        password_label.setStyleSheet("""
            color: white;
            font-size: 9px;
            font-weight: 600;
        """)
        layout.addWidget(password_label)

        self.login_password = QLineEdit()
        self.login_password.setObjectName("login-password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.setStyleSheet(self.get_input_style())
        self.login_password.returnPressed.connect(self.handle_login)
        layout.addWidget(self.login_password)

        layout.addSpacing(10)

        # LOGIN BUTTON - LARGE AND VISIBLE
        login_btn = QPushButton("LOG IN")
        login_btn.setMinimumHeight(40)
        login_btn.setMinimumWidth(120)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6,
                    stop:1 #2563eb);
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 6px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb,
                    stop:1 #1d4ed8);
            }
            QPushButton:pressed {
                background: #1e40af;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)

        layout.addStretch()
        return widget

    def apply_theme(self, theme: str):
        """Adjust dialog styles for light/dark theme with proper backgrounds and text colors."""
        if theme == 'light':
            # Light theme background
            self.setStyleSheet("""QDialog { background: #f8fafc; }""")
            
            # Update tab styles for light mode
            self.tabs.setStyleSheet("""
                QTabWidget::pane { background: transparent; border: none; }
                QTabBar::tab { 
                    background: transparent; 
                    color: #64748b; 
                    padding: 10px 28px; 
                    font-size: 15px; 
                    font-weight: 600;
                    border: none;
                }
                QTabBar::tab:selected { 
                    color: #0f172a; 
                    border-bottom: 3px solid #3b82f6; 
                }
                QTabBar::tab:hover {
                    color: #475569;
                }
            """)
            
            # Update all labels to dark text for light background
            for lbl in self.findChildren(QLabel):
                lbl.setStyleSheet("""
                    color: #0f172a;
                    font-weight: 600;
                    font-size: 10px;
                """)
            
            # Update all input fields for light theme
            for inp in self.findChildren(QLineEdit):
                inp.setStyleSheet("""
                    QLineEdit {
                        background: white;
                        border: 2px solid #cbd5e1;
                        border-radius: 8px;
                        padding: 10px;
                        color: #0f172a;
                        font-size: 10px;
                        selection-background-color: #3b82f6;
                    }
                    QLineEdit:focus {
                        border: 2px solid #3b82f6;
                        background: #f0f9ff;
                    }
                    QLineEdit::placeholder {
                        color: #94a3b8;
                    }
                """)
            
            # Update button styles
            for btn in self.findChildren(QPushButton):
                text = btn.text().upper()
                if 'LOG IN' in text:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #3b82f6, stop:1 #2563eb);
                            color: white;
                            border: none;
                            border-radius: 10px;
                            font-weight: bold;
                            font-size: 8px;
                            padding: 4px;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #2563eb, stop:1 #1d4ed8);
                        }
                    """)
                elif 'CREATE ACCOUNT' in text:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #10b981, stop:1 #059669);
                            color: white;
                            border: none;
                            border-radius: 10px;
                            font-weight: bold;
                            font-size: 10px;
                            padding: 10px;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #059669, stop:1 #047857);
                        }
                    """)
                elif 'CONTINUE' in text:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: transparent;
                            border: 2px solid #cbd5e1;
                            border-radius: 8px;
                            color: #64748b;
                            padding: 8px;
                            font-size: 12px;
                            font-weight: 600;
                        }
                        QPushButton:hover {
                            border-color: #94a3b8;
                            color: #0f172a;
                            background: rgba(15, 23, 42, 0.05);
                        }
                    """)
        else:
            # Dark theme - revert to original defaults
            self.setStyleSheet("""QDialog { background: #0f172a; }""")
            
            self.tabs.setStyleSheet("""
                QTabWidget::pane { border: none; background: transparent; }
                QTabBar::tab { 
                    background: transparent; 
                    color: #64748b; 
                    padding: 10px 28px; 
                    font-size: 15px; 
                    font-weight: 600; 
                    border: none;
                }
                QTabBar::tab:selected { 
                    color: white; 
                    border-bottom: 3px solid #3b82f6; 
                }
                QTabBar::tab:hover {
                    color: #cbd5e1;
                }
            """)
            
            # Revert labels to white
            for lbl in self.findChildren(QLabel):
                lbl.setStyleSheet("""
                    color: white;
                    font-weight: 600;
                    font-size: 10px;
                """)
            
            # Revert input fields to dark theme
            for inp in self.findChildren(QLineEdit):
                inp.setStyleSheet(self.get_input_style())
            
            # Revert button styles to dark theme defaults
            for btn in self.findChildren(QPushButton):
                text = btn.text().upper()
                if 'LOG IN' in text:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #3b82f6, stop:1 #2563eb);
                            color: white;
                            border: none;
                            border-radius: 10px;
                            font-weight: bold;
                            font-size: 10px;
                            padding: 10px;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #2563eb, stop:1 #1d4ed8);
                        }
                    """)
                elif 'CREATE ACCOUNT' in text:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #10b981, stop:1 #059669);
                            color: white;
                            border: none;
                            border-radius: 10px;
                            font-weight: bold;
                            font-size: 10px;
                            padding: 10px;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #059669, stop:1 #047857);
                        }
                    """)
                elif 'CONTINUE' in text:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: transparent;
                            border: 2px solid #475569;
                            border-radius: 8px;
                            color: #94a3b8;
                            padding: 8px;
                            font-size: 12px;
                            font-weight: 600;
                        }
                        QPushButton:hover {
                            border-color: #64748b;
                            color: #cbd5e1;
                            background: rgba(100, 116, 139, 0.1);
                        }
                    """)

    def create_register_tab(self):
        """Create register tab with clear, visible buttons"""
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 16, 0, 16)
        layout.setSpacing(12)

        # Username
        username_label = QLabel("Username")
        username_label.setStyleSheet("""
            color: white;
            font-size: 9px;
            font-weight: 600;
        """)
        layout.addWidget(username_label)

        self.register_username = QLineEdit()
        self.register_username.setObjectName("register-username")
        self.register_username.setPlaceholderText("Choose a username")
        self.register_username.setStyleSheet(self.get_input_style())
        layout.addWidget(self.register_username)

        # Email
        email_label = QLabel("Email")
        email_label.setStyleSheet("""
            color: white;
            font-size: 9px;
            font-weight: 600;
        """)
        layout.addWidget(email_label)

        self.register_email = QLineEdit()
        self.register_email.setObjectName("register-email")
        self.register_email.setPlaceholderText("your@email.com")
        self.register_email.setStyleSheet(self.get_input_style())
        layout.addWidget(self.register_email)

        # Password
        password_label = QLabel("Password")
        password_label.setStyleSheet("""
            color: white;
            font-size: 9px;
            font-weight: 600;
        """)
        layout.addWidget(password_label)

        self.register_password = QLineEdit()
        self.register_password.setObjectName("register-password")
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setPlaceholderText("Min 8 characters")
        self.register_password.setStyleSheet(self.get_input_style())
        self.register_password.returnPressed.connect(self.handle_register)
        layout.addWidget(self.register_password)

        layout.addSpacing(10)

        # REGISTER BUTTON - LARGE AND VISIBLE
        register_btn = QPushButton("CREATE ACCOUNT")
        register_btn.setMinimumHeight(40)
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #10b981,
                    stop:1 #059669);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 0.5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #059669,
                    stop:1 #047857);
            }
            QPushButton:pressed {
                background: #065f46;
            }
        """)
        register_btn.clicked.connect(self.handle_register)
        layout.addWidget(register_btn)

        layout.addStretch()
        return widget

    def get_input_style(self):
        """Consistent input field styling"""
        return """
            QLineEdit {
                background: #1e293b;
                border: 2px solid #334155;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
                background: #1e293b;
            }
            QLineEdit::placeholder {
                color: #64748b;
            }
        """

    def handle_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()

        if not username or not password:
            QMessageBox.warning(
                self, 
                "Missing Information", 
                "Please enter both username and password"
            )
            return

        try:
            result = self.api_client.login(username, password)
            self.user_data = result.get("user")
            QMessageBox.information(
                self, 
                "Success", 
                f"Welcome back, {username}!"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Login Failed", 
                f"Unable to login:\n\n{str(e)}"
            )

    def handle_register(self):
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text().strip()

        if not username or not email or not password:
            QMessageBox.warning(
                self, 
                "Missing Information", 
                "Please fill in all fields"
            )
            return

        if len(password) < 8:
            QMessageBox.warning(
                self,
                "Weak Password",
                "Password must be at least 8 characters long"
            )
            return

        if "@" not in email or "." not in email:
            QMessageBox.warning(
                self,
                "Invalid Email",
                "Please enter a valid email address"
            )
            return

        try:
            result = self.api_client.register(username, email, password)
            self.user_data = result.get("user")
            QMessageBox.information(
                self, 
                "Success", 
                f"Account created successfully!\nWelcome, {username}!"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Registration Failed", 
                f"Unable to create account:\n\n{str(e)}"
            )