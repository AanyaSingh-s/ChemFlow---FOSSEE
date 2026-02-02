# desktop/gui/index_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from gui.animated_background import AnimatedBackground


class IndexPage(AnimatedBackground):
    
    def __init__(self, main_window=None):
        super().__init__(main_window)

        self.main_window = main_window

        # ============================================================
        # MAIN ROOT LAYOUT
        # ============================================================
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # --------- CENTERED CONTAINER (like max-w-7xl) ---------
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: transparent;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(60, 40, 60, 40)
        container_layout.setSpacing(40)

        root.addWidget(container, 0, Qt.AlignTop | Qt.AlignHCenter)
        container.setMaximumWidth(1400)    
        # ============================================================
        # NAVBAR
        # ============================================================
        nav = QHBoxLayout()
        nav.setSpacing(20)

        brand = QLabel(
            "<span style='font-size:10px; letter-spacing:2px; "
            "color:#bfdbfe;'>CHEMFLOW ANALYTICS</span><br>"
            "<span style='font-size:15px; font-weight:800; color:white;'>"
            "Chemical Equipment Intelligence</span>"
        )
        nav.addWidget(brand)
        nav.addStretch()

        self.btn_login = QPushButton("Log In")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setStyleSheet(self._nav_button())
        nav.addWidget(self.btn_login)

        self.btn_get_started = QPushButton("Get Started")
        self.btn_get_started.setCursor(Qt.PointingHandCursor)
        self.btn_get_started.setStyleSheet(self._nav_button(primary=True))
        nav.addWidget(self.btn_get_started)
        
        # Theme toggle (emoji icon) - calls main_window.toggle_theme
        self.btn_toggle_theme = QPushButton("🌙")
        self.btn_toggle_theme.setCursor(Qt.PointingHandCursor)
        self.btn_toggle_theme.setStyleSheet("QPushButton{ background: transparent; border: none; font-size:16px; } QPushButton:hover{opacity:0.8}")
        nav.addWidget(self.btn_toggle_theme)

        container_layout.addLayout(nav)

        # ============================================================
        # HERO SECTION
        # ============================================================
        hero = QHBoxLayout()
        hero.setSpacing(40)

        # ---------------- LEFT SIDE ----------------
        left = QVBoxLayout()
        left.setSpacing(25)

        pill = QLabel(
            "<span style='color:#22c55e;'>●</span> "
            "<span style='color:#e5e7eb;'>Real-time CSV analytics for modern process labs</span>"
        )
        pill.setStyleSheet("""
            background: rgba(15,23,42,0.70);
            padding: 6px 16px;
            border-radius: 20px;
        """)
        left.addWidget(pill, 0, Qt.AlignLeft)

        self.heading = QLabel(
            "Upload, analyze, and\nvisualize chemical\nequipment datasets in\nseconds."
        )
        self.heading.setStyleSheet("color:white; font-size:28px; font-weight:800;")
        self.heading.setWordWrap(True)
        left.addWidget(self.heading)

        self.subtitle = QLabel(
            "Flow-rate trends, pressure deviations, temperature correlations, and more. "
            "Unlock insights from every CSV using interactive dashboards built for "
            "process engineers and researchers."
        )
        self.subtitle.setWordWrap(True)
        self.subtitle.setStyleSheet("color:#d1d5db; font-size:15px;")
        left.addWidget(self.subtitle)

        # Buttons
        ctas = QHBoxLayout()
        ctas.setSpacing(20)

        self.btn_create_workspace = QPushButton("Create your workspace")
        self.btn_create_workspace.setMinimumHeight(42)
        self.btn_create_workspace.setCursor(Qt.PointingHandCursor)
        self.btn_create_workspace.setStyleSheet(self._cta_primary())
        ctas.addWidget(self.btn_create_workspace)

        self.btn_view_dashboard = QPushButton("View dashboard")
        self.btn_view_dashboard.setMinimumHeight(42)
        self.btn_view_dashboard.setCursor(Qt.PointingHandCursor)
        self.btn_view_dashboard.setStyleSheet(self._cta_secondary())
        ctas.addWidget(self.btn_view_dashboard)

        left.addLayout(ctas)
        hero.addLayout(left, 2)

        # ---------------- RIGHT SIDE CARD PANEL ----------------
        card = QFrame()
        card.setMinimumWidth(450)
        card.setMaximumWidth(480)
        card.setStyleSheet("""
            QFrame {
                background: rgba(15,23,42,0.75);
                border: 1px solid rgba(148,163,184,0.35);
                border-radius: 22px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)

        def add_feature(title, desc):
            block = QFrame()
            block.setStyleSheet("""
                QFrame {
                    background: rgba(255,255,255,0.02);
                    border: 1px solid rgba(100,116,139,0.25);
                    border-radius: 18px;
                }
            """)
            b_layout = QVBoxLayout(block)
            b_layout.setContentsMargins(18, 15, 18, 15)

            t = QLabel(f"<b style='color:white; font-size:16px;'>{title}</b>")
            d = QLabel(desc)
            d.setStyleSheet("color:#cbd5e1; font-size:13px;")
            d.setWordWrap(True)

            b_layout.addWidget(t)
            b_layout.addWidget(d)

            card_layout.addWidget(block)

        add_feature("1. Upload CSV", "Drag, drop, and validate your process data.")
        add_feature("2. Visualize Instantly", "Interactive charts and KPIs with zero config.")
        add_feature("3. Track Safely", "Secure login, history controls, and reproducible records.")

        hero.addWidget(card, 1)

        container_layout.addLayout(hero)

        # ============================================================
        # SIGNALS
        # ============================================================
        if self.main_window:
            self.btn_login.clicked.connect(self.main_window.show_login)
            self.btn_get_started.clicked.connect(self.main_window.show_login)
            self.btn_create_workspace.clicked.connect(self.main_window.show_login)
            self.btn_view_dashboard.clicked.connect(self.main_window.show_dashboard_page)
            self.btn_toggle_theme.clicked.connect(self.main_window.toggle_theme)

            # Apply current theme on init
            try:
                self.apply_theme(self.main_window.theme)
            except Exception:
                pass

    # ============================================================
    # STYLE HELPERS
    # ============================================================
    def _nav_button(self, primary=False):
        if primary:
            return """
                QPushButton {
                    background:#3b82f6;
                    color:white;
                    padding:10px 22px;
                    border-radius:10px;
                    font-size:12px;
                    font-weight:600;
                }
                QPushButton:hover { background:#2563eb; }
            """
        return """
            QPushButton {
                background:#1e293b;
                color:white;
                padding:10px 22px;
                border-radius:10px;
                font-size:11px;
                font-weight:600;
                border:1px solid rgba(255,255,255,0.1);
            }
            QPushButton:hover { background:#334155; }
        """

    def apply_theme(self, theme: str):
        """Apply light or dark theme to desktop index page UI elements."""
        if theme == 'light':
            # Nav
            self.btn_login.setStyleSheet("QPushButton{background: transparent; color: #0f172a; padding:8px 16px; border-radius:8px; border:1px solid rgba(15,23,42,0.06)}")
            self.btn_get_started.setStyleSheet("QPushButton{background:#3b82f6; color:white; padding:8px 16px; border-radius:8px}")
            self.btn_create_workspace.setStyleSheet("QPushButton{background:#3b82f6; color:white; border-radius:12px; padding:10px 18px}")
            self.btn_view_dashboard.setStyleSheet("QPushButton{background: transparent; color:#0f172a; border:1px solid rgba(15,23,42,0.06); border-radius:12px; padding:10px 18px}")
            self.btn_toggle_theme.setText('☀️')
            # Heading/subtitle colors
            self.heading.setStyleSheet("color:#0f172a; font-size:28px; font-weight:800;")
            self.subtitle.setStyleSheet("color:#334155; font-size:15px;")
        else:
            # dark
            self.btn_login.setStyleSheet(self._nav_button())
            self.btn_get_started.setStyleSheet(self._nav_button(primary=True))
            self.btn_create_workspace.setStyleSheet(self._cta_primary())
            self.btn_view_dashboard.setStyleSheet(self._cta_secondary())
            self.btn_toggle_theme.setText('🌙')
            self.heading.setStyleSheet("color:white; font-size:28px; font-weight:800;")
            self.subtitle.setStyleSheet("color:#d1d5db; font-size:15px;")

    def _cta_primary(self):
        return """
            QPushButton {
                background:#3b82f6;
                color:white;
                border-radius:12px;
                font-size:11px;
                font-weight:600;
            }
            QPushButton:hover { background:#2563eb; }
        """

    def _cta_secondary(self):
        return """
            QPushButton {
                background:#1e293b;
                color:white;
                border-radius:12px;
                font-size:11px;
                font-weight:600;
                border:1px solid rgba(255,255,255,0.25);
            }
            QPushButton:hover { background:#334155; }
        """
