from __future__ import annotations

import platform
from typing import TYPE_CHECKING

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QRadialGradient
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from pymymc import constants
from pymymc.log import log_info
from pymymc.ui.home_page import HomePage
from pymymc.ui.settings_page import SettingsPage
from pymymc.ui.versions_page import VersionsPage

if TYPE_CHECKING:
    from pymymc.app import App

_ICON_HOME = "\u2302"
_ICON_VERSIONS = "\u229e"
_ICON_SETTINGS = "\u2699"
_ICON_CLOSE = "\u2715"

_SYSTEM = platform.system()
_FONT_FAMILY = {
    "Darwin": "Helvetica Neue",
    "Windows": "Segoe UI",
}.get(_SYSTEM, "Noto Sans")

_STYLESHEET = f"""
/* ── Global ── */
QWidget {{
    background-color: {constants.ui.BG_PRIMARY};
    color: {constants.ui.TEXT_PRIMARY};
    font-family: "{_FONT_FAMILY}";
    font-size: 13px;
}}

QLabel {{
    background-color: transparent;
}}

/* ── Close button ── */
QPushButton#close_btn {{
    background: transparent;
    border: none;
    color: {constants.ui.TEXT_SECONDARY};
    font-size: 14px;
    padding: 0;
}}

QPushButton#close_btn:hover {{
    background: {constants.ui.DANGER};
    color: white;
}}

/* ── Sidebar ── */
QWidget#sidebar {{
    background-color: {constants.ui.BG_DARKEST};
}}

QPushButton.sidebar_btn {{
    background: transparent;
    border: none;
    border-left: 3px solid transparent;
    color: {constants.ui.TEXT_SECONDARY};
    padding: 14px 0;
    font-size: 11px;
}}

QPushButton.sidebar_btn:checked {{
    border-left: 3px solid {constants.ui.ACCENT};
    color: {constants.ui.TEXT_PRIMARY};
    background: {constants.ui.BG_PRIMARY};
}}

QPushButton.sidebar_btn:hover {{
    color: {constants.ui.TEXT_PRIMARY};
}}

/* ── Page titles ── */
QLabel#page_title {{
    font-size: 20px;
    font-weight: bold;
}}

QLabel#page_title_logo {{
    font-size: 24px;
    font-weight: bold;
}}

QLabel#page_desc {{
    color: {constants.ui.TEXT_SECONDARY};
    font-size: 12px;
}}

QLabel#subtitle {{
    color: {constants.ui.TEXT_SECONDARY};
    font-size: 12px;
}}

QLabel#card_heading {{
    font-size: 13px;
    font-weight: bold;
    color: {constants.ui.ACCENT_LIGHT};
}}

/* ── Status bar ── */
QLabel#status_version {{
    font-size: 10px;
    color: {constants.ui.TEXT_DISABLED};
}}

QLabel#status_dot_online {{
    color: {constants.ui.SUCCESS};
    font-size: 10px;
}}

QLabel#status_dot_offline {{
    color: {constants.ui.DANGER};
    font-size: 10px;
}}

QLabel#status_text {{
    font-size: 10px;
    color: {constants.ui.TEXT_SECONDARY};
}}

/* ── Cards ── */
QFrame#card {{
    background: {constants.ui.BG_SURFACE};
    border: 1px solid {constants.ui.BORDER_SUBTLE};
    border-radius: 10px;
    padding: 16px;
}}

/* ── Inputs ── */
QLineEdit {{
    background-color: {constants.ui.BG_ELEVATED};
    border: 1px solid {constants.ui.BORDER};
    border-radius: 4px;
    padding: 6px;
    color: {constants.ui.TEXT_PRIMARY};
}}

QLineEdit:focus {{
    border: 1px solid {constants.ui.ACCENT};
}}

QComboBox {{
    background-color: {constants.ui.BG_ELEVATED};
    border: 1px solid {constants.ui.BORDER};
    border-radius: 4px;
    padding: 6px;
    color: {constants.ui.TEXT_PRIMARY};
}}

QComboBox:focus {{
    border: 1px solid {constants.ui.ACCENT};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox QAbstractItemView {{
    background-color: {constants.ui.BG_ELEVATED};
    border: 1px solid {constants.ui.BORDER};
    color: {constants.ui.TEXT_PRIMARY};
    selection-background-color: {constants.ui.ACCENT};
}}

/* ── Buttons ── */
QPushButton {{
    background-color: {constants.ui.ACCENT};
    color: {constants.ui.TEXT_PRIMARY};
    font-weight: bold;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
}}

QPushButton:hover {{
    background-color: {constants.ui.ACCENT_LIGHT};
}}

QPushButton:pressed {{
    background-color: {constants.ui.ACCENT};
}}

QPushButton#delete_button {{
    background-color: {constants.ui.DANGER};
}}

QPushButton#delete_button:hover {{
    background-color: {constants.ui.DANGER_HOVER};
}}

/* ── Play button ── */
QPushButton#play_button {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {constants.ui.ACCENT}, stop:1 {constants.ui.ACCENT_GRADIENT_END});
    border: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: bold;
    padding: 12px 0;
    color: white;
}}

QPushButton#play_button:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {constants.ui.ACCENT_LIGHT}, stop:1 #C084FC);
}}

/* ── Checkboxes ── */
QCheckBox {{
    background: transparent;
    color: {constants.ui.TEXT_SECONDARY};
    spacing: 6px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 3px;
    border: 1px solid {constants.ui.BORDER};
    background-color: {constants.ui.BG_ELEVATED};
}}

QCheckBox::indicator:checked {{
    background-color: {constants.ui.ACCENT};
    border: 1px solid {constants.ui.ACCENT};
}}

/* ── Progress bar ── */
QProgressBar {{
    background-color: {constants.ui.BG_ELEVATED};
    border: none;
    border-radius: 4px;
    text-align: center;
    color: {constants.ui.TEXT_PRIMARY};
    font-size: 11px;
}}

QProgressBar::chunk {{
    background-color: {constants.ui.ACCENT};
    border-radius: 4px;
}}

/* ── Group boxes ── */
QGroupBox {{
    font-weight: bold;
    border: 1px solid {constants.ui.BORDER};
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 16px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: {constants.ui.TEXT_SECONDARY};
}}

/* ── Spin boxes ── */
QSpinBox {{
    background-color: {constants.ui.BG_ELEVATED};
    border: 1px solid {constants.ui.BORDER};
    border-radius: 4px;
    padding: 6px;
    color: {constants.ui.TEXT_PRIMARY};
}}

QSpinBox:focus {{
    border: 1px solid {constants.ui.ACCENT};
}}

/* ── List widget ── */
QListWidget {{
    background-color: {constants.ui.BG_ELEVATED};
    border: 1px solid {constants.ui.BORDER};
    border-radius: 4px;
    color: {constants.ui.TEXT_PRIMARY};
    padding: 4px;
}}

QListWidget::item {{
    padding: 4px 8px;
    border-radius: 3px;
}}

QListWidget::item:selected {{
    background-color: {constants.ui.ACCENT};
}}

QListWidget::item:hover {{
    background-color: {constants.ui.BORDER};
}}

/* ── Scrollbars ── */
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
}}

QScrollBar::handle:vertical {{
    background: {constants.ui.BORDER};
    border-radius: 3px;
    min-height: 24px;
}}

QScrollBar::handle:vertical:hover {{
    background: {constants.ui.TEXT_SECONDARY};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 6px;
}}

QScrollBar::handle:horizontal {{
    background: {constants.ui.BORDER};
    border-radius: 3px;
    min-width: 24px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {constants.ui.TEXT_SECONDARY};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: transparent;
}}

/* ── Scroll area ── */
QScrollArea {{
    background: transparent;
    border: none;
}}

/* ── Segmented control ── */
QFrame#segment_container {{
    background-color: {constants.ui.BG_ELEVATED};
    border: 1px solid {constants.ui.BORDER};
    border-radius: 16px;
}}

QPushButton#segment_btn {{
    background: transparent;
    border: none;
    border-radius: 13px;
    color: {constants.ui.TEXT_SECONDARY};
    font-size: 12px;
    font-weight: bold;
    padding: 6px 0;
}}

QPushButton#segment_btn:checked {{
    background-color: {constants.ui.ACCENT};
    color: {constants.ui.TEXT_PRIMARY};
}}

QPushButton#segment_btn:hover:!checked {{
    color: {constants.ui.TEXT_PRIMARY};
}}

/* ── Glow transparency ── */
QStackedWidget {{
    background: transparent;
}}

QStackedWidget > QWidget {{
    background: transparent;
}}
"""


class _GlowBackground(QWidget):
    def paintEvent(self, event: object) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.fillRect(self.rect(), QColor(constants.ui.BG_PRIMARY))

        w, h = self.width(), self.height()
        gradient = QRadialGradient(
            w * constants.ui.GLOW_ORIGIN_X,
            h * constants.ui.GLOW_ORIGIN_Y,
            max(w, h) * constants.ui.GLOW_RADIUS_FACTOR,
        )

        glow = QColor(constants.ui.GLOW_COLOUR)
        glow.setAlphaF(constants.ui.GLOW_OPACITY)
        gradient.setColorAt(0.0, glow)
        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))

        p.fillRect(self.rect(), gradient)
        p.end()


class _DraggableWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._drag_pos: QPoint | None = None

    def mousePressEvent(self, event: object) -> None:
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: object) -> None:
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: object) -> None:
        self._drag_pos = None


class _SidebarButton(QPushButton):
    def __init__(self, icon_text: str, label: str) -> None:
        super().__init__(f"{icon_text}\n{label}")
        self.setCheckable(True)
        self.setProperty("class", "sidebar_btn")
        self.setFixedWidth(56)


class MainWindow:
    def __init__(self, app: App) -> None:
        self._app = app
        self._build()
        app.set_ui_refresh(self._on_config_changed)

    def _build(self) -> None:
        log_info("Configuring the UI...")

        qt_app = QApplication.instance()
        qt_app.setStyleSheet(_STYLESHEET)

        self._window = _DraggableWindow()
        self._window.setWindowTitle("PyMyMC")
        self._window.setWindowIcon(QIcon(constants.ui.LOGO_ICON))
        self._window.setWindowFlags(Qt.FramelessWindowHint)
        self._window.setFixedSize(720, 520)

        root = QHBoxLayout(self._window)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        body = root

        # Sidebar
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(56)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 4, 0, 4)
        sidebar_layout.setSpacing(0)

        self._btn_group = QButtonGroup(self._window)
        self._btn_group.setExclusive(True)

        home_btn = _SidebarButton(_ICON_HOME, "Home")
        versions_btn = _SidebarButton(_ICON_VERSIONS, "Versions")
        settings_btn = _SidebarButton(_ICON_SETTINGS, "Settings")

        for i, btn in enumerate((home_btn, versions_btn, settings_btn)):
            self._btn_group.addButton(btn, i)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Status area at bottom of sidebar
        version_label = QLabel(f"v{self._app.version}")
        version_label.setObjectName("status_version")
        version_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version_label)

        body.addWidget(sidebar)

        # Stacked content with glow background
        content_area = _GlowBackground()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self._stack = QStackedWidget()

        self._home_page = HomePage(self._app)
        self._versions_page = VersionsPage(self._app)
        self._settings_page = SettingsPage(self._app)

        self._stack.addWidget(self._home_page)
        self._stack.addWidget(self._versions_page)
        self._stack.addWidget(self._settings_page)

        content_layout.addWidget(self._stack)
        body.addWidget(content_area, 1)

        # Close button
        close_btn = QPushButton(_ICON_CLOSE, self._window)
        close_btn.setObjectName("close_btn")
        close_btn.setFixedSize(28, 28)
        close_btn.move(self._window.width() - 28, 0)
        close_btn.raise_()
        close_btn.clicked.connect(self._window.close)

        # Wire sidebar to stack
        self._btn_group.buttonClicked[int].connect(self._stack.setCurrentIndex)
        home_btn.setChecked(True)

        # Initial data load
        self._home_page.refresh()

        log_info("Done!")

    def _on_config_changed(self) -> None:
        self._home_page.refresh()

    def run(self) -> None:
        self._window.show()
        QApplication.instance().exec_()
