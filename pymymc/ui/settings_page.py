from __future__ import annotations

import platform
import re
from pathlib import Path
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from pymymc import constants

if TYPE_CHECKING:
    from pymymc.app import App

_ICON_DOT = "\u25cf"

_SYSTEM = platform.system()


def _make_card(title: str) -> tuple[QFrame, QVBoxLayout]:
    card = QFrame()
    card.setObjectName("card")
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(24)
    shadow.setOffset(0, 6)
    shadow.setColor(Qt.black)
    card.setGraphicsEffect(shadow)

    card_layout = QVBoxLayout(card)
    card_layout.setContentsMargins(16, 16, 16, 16)
    card_layout.setSpacing(10)

    heading = QLabel(title)
    heading.setObjectName("card_heading")
    card_layout.addWidget(heading)

    return card, card_layout


class SettingsPage(QWidget):
    def __init__(self, app: App, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._app = app
        self._build()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outer.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Settings")
        title.setObjectName("page_title")
        layout.addWidget(title)

        desc = QLabel("Configure your launcher")
        desc.setObjectName("page_desc")
        layout.addWidget(desc)

        online = self._app.has_internet
        status_row = QHBoxLayout()
        status_row.setSpacing(6)
        dot = QLabel(_ICON_DOT)
        dot.setObjectName("status_dot_online" if online else "status_dot_offline")
        status_row.addWidget(dot)
        status_label = QLabel("Online" if online else "Offline")
        status_label.setObjectName("status_text")
        status_row.addWidget(status_label)
        status_row.addStretch()
        layout.addLayout(status_row)

        config = self._app.config

        # Paths
        paths_card, paths_layout = _make_card("Paths")

        paths_layout.addWidget(QLabel("Minecraft Directory:"))
        mc_row = QHBoxLayout()
        self._mc_path_entry = QLineEdit(str(config.minecraft_dir))
        mc_row.addWidget(self._mc_path_entry, 1)
        mc_browse = QPushButton("Browse")
        mc_browse.clicked.connect(self._browse_mc_dir)
        mc_row.addWidget(mc_browse)
        paths_layout.addLayout(mc_row)

        paths_layout.addWidget(QLabel("Java Executable:"))
        java_row = QHBoxLayout()
        self._java_path_entry = QLineEdit(config.java_path)
        self._java_path_entry.setPlaceholderText("System default")
        java_row.addWidget(self._java_path_entry, 1)
        java_browse = QPushButton("Browse")
        java_browse.clicked.connect(self._browse_java)
        java_row.addWidget(java_browse)
        paths_layout.addLayout(java_row)

        layout.addWidget(paths_card)

        # Performance
        perf_card, perf_layout = _make_card("Performance")

        perf_layout.addWidget(QLabel("Dedicated RAM:"))
        ram_row = QHBoxLayout()
        self._ram_spin = QSpinBox()
        self._ram_spin.setMinimum(1)
        self._ram_spin.setMaximum(64)
        self._ram_spin.setSuffix(" GB")

        xmx_match = re.search(r"-Xmx(\d+)G", config.jvm_args)
        self._ram_spin.setValue(int(xmx_match.group(1)) if xmx_match else 2)

        ram_row.addWidget(self._ram_spin)
        ram_row.addStretch()
        perf_layout.addLayout(ram_row)

        perf_layout.addWidget(QLabel("JVM Arguments:"))
        self._jvm_args_entry = QLineEdit(config.jvm_args)
        self._jvm_args_entry.setPlaceholderText("-Xmx2G -XX:+UseG1GC")
        perf_layout.addWidget(self._jvm_args_entry)

        self._ram_spin.valueChanged.connect(self._on_ram_changed)

        layout.addWidget(perf_card)

        # Display
        display_card, display_layout = _make_card("Display")

        self._resolution_check = QCheckBox("Use custom resolution")
        self._resolution_check.setChecked(config.custom_resolution)
        display_layout.addWidget(self._resolution_check)

        res_row = QHBoxLayout()
        self._width_spin = QSpinBox()
        self._width_spin.setMinimum(320)
        self._width_spin.setMaximum(7680)
        self._width_spin.setValue(config.resolution_width)
        res_row.addWidget(self._width_spin)
        res_row.addWidget(QLabel("x"))
        self._height_spin = QSpinBox()
        self._height_spin.setMinimum(240)
        self._height_spin.setMaximum(4320)
        self._height_spin.setValue(config.resolution_height)
        res_row.addWidget(self._height_spin)
        res_row.addStretch()
        display_layout.addLayout(res_row)

        self._width_spin.setEnabled(config.custom_resolution)
        self._height_spin.setEnabled(config.custom_resolution)
        self._resolution_check.toggled.connect(self._width_spin.setEnabled)
        self._resolution_check.toggled.connect(self._height_spin.setEnabled)

        layout.addWidget(display_card)

        # Quick Connect
        connect_card, connect_layout = _make_card("Quick Connect")

        connect_row = QHBoxLayout()
        self._server_entry = QLineEdit(config.auto_connect_server)
        self._server_entry.setPlaceholderText("Server IP")
        connect_row.addWidget(self._server_entry, 1)
        connect_row.addWidget(QLabel(":"))
        self._port_spin = QSpinBox()
        self._port_spin.setMinimum(1)
        self._port_spin.setMaximum(65535)
        self._port_spin.setValue(config.auto_connect_port)
        self._port_spin.setMaximumWidth(80)
        connect_row.addWidget(self._port_spin)
        connect_layout.addLayout(connect_row)

        layout.addWidget(connect_card)

        # Game
        game_card, game_layout = _make_card("Game")

        self._historical_check = QCheckBox("Show non-release versions")
        self._historical_check.setChecked(config.show_historical)
        game_layout.addWidget(self._historical_check)

        layout.addWidget(game_card)

        # Forget me
        self._forget_me_check = QCheckBox("Forget my account details")
        self._forget_me_check.setStyleSheet(
            f"color: {constants.ui.WARNING};",
        )
        layout.addWidget(self._forget_me_check)

        # Apply
        button_row = QHBoxLayout()
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self._apply)
        button_row.addWidget(apply_btn)
        button_row.addStretch()
        layout.addLayout(button_row)

    def _on_ram_changed(self, value: int) -> None:
        text = self._jvm_args_entry.text()
        new_flag = f"-Xmx{value}G"
        if re.search(r"-Xmx\d+G", text):
            text = re.sub(r"-Xmx\d+G", new_flag, text)
        elif text.strip():
            text = new_flag + " " + text
        else:
            text = new_flag
        self._jvm_args_entry.setText(text)

    def _browse_mc_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(
            self,
            "Select Minecraft Directory",
            self._mc_path_entry.text(),
        )
        if path:
            self._mc_path_entry.setText(path)

    def _browse_java(self) -> None:
        file_filter = "Executables (*.exe)" if _SYSTEM == "Windows" else "All Files (*)"
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Java Executable",
            "",
            file_filter,
        )
        if path:
            self._java_path_entry.setText(path)

    def _apply(self) -> None:
        config = self._app.config

        mc_path = Path(self._mc_path_entry.text())

        if self._forget_me_check.isChecked():
            config.email = ""
            config.uuid = ""
            config.access_token = ""

        config.minecraft_dir = mc_path
        config.java_path = self._java_path_entry.text()
        config.jvm_args = self._jvm_args_entry.text()
        config.custom_resolution = self._resolution_check.isChecked()
        config.resolution_width = self._width_spin.value()
        config.resolution_height = self._height_spin.value()
        config.auto_connect_server = self._server_entry.text()
        config.auto_connect_port = self._port_spin.value()
        config.only_releases = not self._historical_check.isChecked()

        self._app.save_config()
        self._app.notify_config_changed()
