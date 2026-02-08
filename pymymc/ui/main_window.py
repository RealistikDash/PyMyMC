from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from pymymc import constants
from pymymc.log import log_info
from pymymc.ui.config_dialogue import ConfigDialogue
from pymymc.ui.dialogues import warning_box
from pymymc.ui.version_manager import VersionManagerDialogue

if TYPE_CHECKING:
    from pymymc.app import App


_STYLESHEET = f"""
QWidget {{
    background-color: {constants.ui.BG_COLOUR};
    color: {constants.ui.TEXT_COLOUR};
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
}}

QLabel {{
    background-color: transparent;
}}

QLineEdit {{
    background-color: {constants.ui.INPUT_BG};
    border: 1px solid {constants.ui.INPUT_BORDER};
    border-radius: 4px;
    padding: 6px;
    color: {constants.ui.TEXT_COLOUR};
}}

QLineEdit:focus {{
    border: 1px solid {constants.ui.ACCENT_COLOUR};
}}

QComboBox {{
    background-color: {constants.ui.INPUT_BG};
    border: 1px solid {constants.ui.INPUT_BORDER};
    border-radius: 4px;
    padding: 6px;
    color: {constants.ui.TEXT_COLOUR};
}}

QComboBox:focus {{
    border: 1px solid {constants.ui.ACCENT_COLOUR};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox QAbstractItemView {{
    background-color: {constants.ui.INPUT_BG};
    border: 1px solid {constants.ui.INPUT_BORDER};
    color: {constants.ui.TEXT_COLOUR};
    selection-background-color: {constants.ui.ACCENT_COLOUR};
}}

QPushButton {{
    background-color: {constants.ui.ACCENT_COLOUR};
    color: {constants.ui.TEXT_COLOUR};
    font-weight: bold;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
}}

QPushButton:hover {{
    background-color: {constants.ui.BUTTON_HOVER};
}}

QPushButton:pressed {{
    background-color: {constants.ui.FG_COLOUR};
}}

QPushButton#cancel_button {{
    background-color: transparent;
    border: 1px solid {constants.ui.ACCENT_COLOUR};
    color: {constants.ui.ACCENT_COLOUR};
}}

QPushButton#cancel_button:hover {{
    background-color: {constants.ui.INPUT_BG};
}}

QPushButton#delete_button {{
    background-color: #F04747;
}}

QPushButton#delete_button:hover {{
    background-color: #D84040;
}}

QCheckBox {{
    color: {constants.ui.TEXT_MUTED};
    spacing: 6px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 3px;
    border: 1px solid {constants.ui.INPUT_BORDER};
    background-color: {constants.ui.INPUT_BG};
}}

QCheckBox::indicator:checked {{
    background-color: {constants.ui.ACCENT_COLOUR};
    border: 1px solid {constants.ui.ACCENT_COLOUR};
}}

QProgressBar {{
    background-color: {constants.ui.INPUT_BG};
    border: none;
    border-radius: 4px;
    text-align: center;
    color: {constants.ui.TEXT_COLOUR};
    font-size: 11px;
}}

QProgressBar::chunk {{
    background-color: {constants.ui.ACCENT_COLOUR};
    border-radius: 4px;
}}

QGroupBox {{
    font-weight: bold;
    border: 1px solid {constants.ui.INPUT_BORDER};
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 16px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: {constants.ui.TEXT_MUTED};
}}

QSpinBox {{
    background-color: {constants.ui.INPUT_BG};
    border: 1px solid {constants.ui.INPUT_BORDER};
    border-radius: 4px;
    padding: 6px;
    color: {constants.ui.TEXT_COLOUR};
}}

QSpinBox:focus {{
    border: 1px solid {constants.ui.ACCENT_COLOUR};
}}

QListWidget {{
    background-color: {constants.ui.INPUT_BG};
    border: 1px solid {constants.ui.INPUT_BORDER};
    border-radius: 4px;
    color: {constants.ui.TEXT_COLOUR};
    padding: 4px;
}}

QListWidget::item {{
    padding: 4px 8px;
    border-radius: 3px;
}}

QListWidget::item:selected {{
    background-color: {constants.ui.ACCENT_COLOUR};
}}

QListWidget::item:hover {{
    background-color: {constants.ui.INPUT_BORDER};
}}
"""


class MainWindow:
    def __init__(self, app: App) -> None:
        self._app = app

        app.set_ui_refresh(self._refresh_versions)

        self._build()

    def _build(self) -> None:
        log_info("Configuring the UI...")

        qt_app = QApplication.instance()
        qt_app.setStyleSheet(_STYLESHEET)

        self._window = QWidget()
        self._window.setWindowTitle("PyMyMC")
        self._window.setWindowIcon(QIcon(constants.ui.LOGO_ICON))
        self._window.setFixedSize(380, 520)

        layout = QVBoxLayout(self._window)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(8)

        logo_pixmap = QPixmap(constants.ui.LOGO_SMALL)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        title_label = QLabel(f"PyMyMC {self._app.version}")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        subtitle_label = QLabel("Made by RealistikDash")
        subtitle_label.setStyleSheet(
            f"font-size: 12px; color: {constants.ui.TEXT_MUTED};",
        )
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"color: {constants.ui.INPUT_BORDER};")
        layout.addWidget(separator)

        self._username_label = QLabel("Email:")
        layout.addWidget(self._username_label)

        self._username_entry = QLineEdit(self._app.config.email)
        layout.addWidget(self._username_entry)

        layout.addWidget(QLabel("Password:"))

        self._password_entry = QLineEdit()
        self._password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self._password_entry)

        layout.addWidget(QLabel("Version:"))

        version_row = QHBoxLayout()
        version_row.setSpacing(8)

        self._version_combo = QComboBox()
        version_row.addWidget(self._version_combo, 1)

        self._remember_me_check = QCheckBox("Remember me")
        version_row.addWidget(self._remember_me_check)

        layout.addLayout(version_row)

        button_row = QHBoxLayout()
        button_row.setSpacing(8)

        play_btn = QPushButton("Play!")
        play_btn.clicked.connect(self._on_play)
        button_row.addWidget(play_btn)

        config_btn = QPushButton("Config")
        config_btn.clicked.connect(self._on_config)
        button_row.addWidget(config_btn)

        versions_btn = QPushButton("Versions")
        versions_btn.clicked.connect(self._on_versions)
        button_row.addWidget(versions_btn)

        layout.addLayout(button_row)

        self._refresh_versions()
        log_info("Done!")

    def _refresh_versions(self) -> None:
        config = self._app.config
        self._username_label.setText("Email:" if config.premium else "Username:")

        versions = self._app.get_versions()
        if config.last_selected and config.last_selected not in versions:
            versions.insert(0, config.last_selected)

        self._version_combo.clear()
        self._version_combo.addItems(versions)

    def _on_play(self) -> None:
        username = self._username_entry.text()
        version = self._version_combo.currentText()
        remember_me = self._remember_me_check.isChecked()

        if not username:
            warning_box("PyMyMC Error!", "Username cannot be empty!")
            return

        if not version:
            warning_box(
                "PyMyMC Error!",
                "No version selected! Download one from the Version Manager.",
            )
            return

        self._window.close()
        self._app.play(
            username=username,
            version=version,
            remember_me=remember_me,
        )

    def _on_config(self) -> None:
        ConfigDialogue(self._window, self._app)

    def _on_versions(self) -> None:
        VersionManagerDialogue(self._window, self._app)
        self._refresh_versions()

    def run(self) -> None:
        self._window.show()
        QApplication.instance().exec_()
