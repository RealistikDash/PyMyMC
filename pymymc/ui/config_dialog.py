from __future__ import annotations

import platform
from typing import TYPE_CHECKING

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from pymymc import constants
from pymymc.ui.dialogs import error_box

if TYPE_CHECKING:
    from pymymc.app import App

_SYSTEM = platform.system()


class ConfigDialog(QDialog):
    def __init__(self, parent: QWidget, app: App) -> None:
        super().__init__(parent)
        self._app = app
        self._app.rpc.set_configuring()
        self._build()
        self.exec_()
        self._app.rpc.set_main_menu()

    def _build(self) -> None:
        config = self._app.config

        self.setWindowTitle("PyMyMC Config")
        self.setWindowIcon(QIcon(constants.ui.LOGO_ICON))
        self.setFixedSize(380, 340)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        warning_label = QLabel(
            "Warning! These options are for advanced users only!",
        )
        layout.addWidget(warning_label)

        caution_label = QLabel("Proceed with caution!")
        caution_label.setStyleSheet(
            f"color: {constants.ui.WARNING_COLOUR}; font-weight: bold;",
        )
        layout.addWidget(caution_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"color: {constants.ui.INPUT_BORDER};")
        layout.addWidget(separator)

        layout.addWidget(QLabel("Minecraft Path:"))

        self._mc_path_entry = QLineEdit(config.minecraft_dir)
        layout.addWidget(self._mc_path_entry)

        layout.addWidget(QLabel("JVM Dedicated RAM:"))

        ram_row = QHBoxLayout()
        ram_row.setSpacing(6)
        self._dram_entry = QLineEdit(str(config.jvm_ram))
        self._dram_entry.setMaximumWidth(80)
        ram_row.addWidget(self._dram_entry)
        ram_row.addWidget(QLabel("GB"))
        ram_row.addStretch()
        layout.addLayout(ram_row)

        self._forget_me_check = QCheckBox("Forget Me")
        layout.addWidget(self._forget_me_check)

        self._premium_check = QCheckBox("Use Premium Minecraft Accounts")
        self._premium_check.setChecked(config.premium)
        layout.addWidget(self._premium_check)

        self._historical_check = QCheckBox("Show non-release versions")
        self._historical_check.setChecked(config.show_historical)
        layout.addWidget(self._historical_check)

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

    def _apply(self) -> None:
        mc_path = self._mc_path_entry.text()
        dram_str = self._dram_entry.text()

        try:
            dram_value = int(dram_str)
            if dram_value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            error_box(
                "PyMyMC Error!",
                "The RAM value has to be an integer (full number) over 0.",
            )
            return

        config = self._app.config

        if self._forget_me_check.isChecked():
            config.email = ""
            config.uuid = ""
            config.access_token = ""

        config.jvm_ram = dram_value

        if _SYSTEM == "Windows":
            if not mc_path.endswith("\\"):
                mc_path += "\\"
        else:
            if not mc_path.endswith("/"):
                mc_path += "/"

        config.minecraft_dir = mc_path
        config.premium = self._premium_check.isChecked()
        config.only_releases = not self._historical_check.isChecked()

        self._app.save_config()
        self.accept()
        self._app.notify_config_changed()
