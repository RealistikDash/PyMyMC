from __future__ import annotations

import platform
import re
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from pymymc import constants

if TYPE_CHECKING:
    from pymymc.app import App

_SYSTEM = platform.system()


class ConfigDialogue(QDialog):
    def __init__(self, parent: QWidget, app: App) -> None:
        super().__init__(parent)
        self._app = app
        self._app.rpc.set_configuring()
        self._build()
        self.exec_()
        self._app.rpc.set_main_menu()

    def _build(self) -> None:
        config = self._app.config

        self.setWindowTitle("PyMyMC Settings")
        self.setWindowIcon(QIcon(constants.ui.LOGO_ICON))
        self.setFixedWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"color: {constants.ui.INPUT_BORDER};")
        layout.addWidget(separator)

        # --- Paths ---
        paths_group = QGroupBox("Paths")
        paths_layout = QVBoxLayout(paths_group)

        paths_layout.addWidget(QLabel("Minecraft Directory:"))
        mc_path_row = QHBoxLayout()
        self._mc_path_entry = QLineEdit(config.minecraft_dir)
        mc_path_row.addWidget(self._mc_path_entry, 1)
        mc_browse_btn = QPushButton("Browse")
        mc_browse_btn.clicked.connect(self._browse_mc_dir)
        mc_path_row.addWidget(mc_browse_btn)
        paths_layout.addLayout(mc_path_row)

        paths_layout.addWidget(QLabel("Java Executable:"))
        java_path_row = QHBoxLayout()
        self._java_path_entry = QLineEdit(config.java_path)
        self._java_path_entry.setPlaceholderText("System default")
        java_path_row.addWidget(self._java_path_entry, 1)
        java_browse_btn = QPushButton("Browse")
        java_browse_btn.clicked.connect(self._browse_java)
        java_path_row.addWidget(java_browse_btn)
        paths_layout.addLayout(java_path_row)

        layout.addWidget(paths_group)

        # --- Performance ---
        perf_group = QGroupBox("Performance")
        perf_layout = QVBoxLayout(perf_group)

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

        layout.addWidget(perf_group)

        # --- Display ---
        display_group = QGroupBox("Display")
        display_layout = QVBoxLayout(display_group)

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

        layout.addWidget(display_group)

        # --- Quick Connect ---
        connect_group = QGroupBox("Quick Connect")
        connect_layout = QHBoxLayout(connect_group)

        self._server_entry = QLineEdit(config.auto_connect_server)
        self._server_entry.setPlaceholderText("Server IP")
        connect_layout.addWidget(self._server_entry, 1)
        connect_layout.addWidget(QLabel(":"))
        self._port_spin = QSpinBox()
        self._port_spin.setMinimum(1)
        self._port_spin.setMaximum(65535)
        self._port_spin.setValue(config.auto_connect_port)
        self._port_spin.setMaximumWidth(80)
        connect_layout.addWidget(self._port_spin)

        layout.addWidget(connect_group)

        # --- Game ---
        game_group = QGroupBox("Game")
        game_layout = QVBoxLayout(game_group)

        self._premium_check = QCheckBox("Use premium Minecraft accounts")
        self._premium_check.setChecked(config.premium)
        game_layout.addWidget(self._premium_check)

        self._historical_check = QCheckBox("Show non-release versions")
        self._historical_check.setChecked(config.show_historical)
        game_layout.addWidget(self._historical_check)

        layout.addWidget(game_group)

        # --- Forget me ---
        self._forget_me_check = QCheckBox("Forget my account details")
        self._forget_me_check.setStyleSheet(
            f"color: {constants.ui.WARNING_COLOUR};",
        )
        layout.addWidget(self._forget_me_check)

        # --- Buttons ---
        button_row = QHBoxLayout()
        button_row.setSpacing(8)

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self._apply)
        button_row.addWidget(apply_btn)

        button_row.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancel_button")
        cancel_btn.clicked.connect(self.reject)
        button_row.addWidget(cancel_btn)

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

        mc_path = self._mc_path_entry.text()
        if _SYSTEM == "Windows":
            if not mc_path.endswith("\\"):
                mc_path += "\\"
        else:
            if not mc_path.endswith("/"):
                mc_path += "/"

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
        config.premium = self._premium_check.isChecked()
        config.only_releases = not self._historical_check.isChecked()

        self._app.save_config()
        self.accept()
        self._app.notify_config_changed()
