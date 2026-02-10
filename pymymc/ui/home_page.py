from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from pymymc import constants
from pymymc.ui.dialogues import warning_box

if TYPE_CHECKING:
    from pymymc.app import App

_ICON_PLAY = "\u25b6"


def _make_card() -> QFrame:
    card = QFrame()
    card.setObjectName("card")
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(24)
    shadow.setOffset(0, 6)
    shadow.setColor(Qt.black)
    card.setGraphicsEffect(shadow)
    return card


class HomePage(QWidget):
    def __init__(self, app: App, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._app = app
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(0)

        layout.addStretch(1)

        logo_pixmap = QPixmap(constants.ui.LOGO_SMALL)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        layout.addSpacing(8)

        title = QLabel("PyMyMC")
        title.setObjectName("page_title_logo")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("by RealistikDash")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        # Segmented control: Premium / Offline
        segment_row = QHBoxLayout()
        segment_row.addStretch()

        segment_container = QFrame()
        segment_container.setObjectName("segment_container")
        segment_container.setFixedHeight(36)
        segment_container.setMaximumWidth(260)
        seg_layout = QHBoxLayout(segment_container)
        seg_layout.setContentsMargins(3, 3, 3, 3)
        seg_layout.setSpacing(0)

        self._premium_btn = QPushButton("Premium")
        self._premium_btn.setObjectName("segment_btn")
        self._premium_btn.setCheckable(True)
        self._premium_btn.setChecked(True)

        self._offline_btn = QPushButton("Offline")
        self._offline_btn.setObjectName("segment_btn")
        self._offline_btn.setCheckable(True)

        self._account_group = QButtonGroup()
        self._account_group.setExclusive(True)
        self._account_group.addButton(self._premium_btn, 0)
        self._account_group.addButton(self._offline_btn, 1)

        seg_layout.addWidget(self._premium_btn, 1)
        seg_layout.addWidget(self._offline_btn, 1)

        segment_row.addWidget(segment_container)
        segment_row.addStretch()
        layout.addLayout(segment_row)

        layout.addSpacing(12)

        card = _make_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        email_row = QHBoxLayout()
        self._username_label = QLabel("Email:")
        self._username_label.setFixedWidth(70)
        email_row.addWidget(self._username_label)
        self._username_entry = QLineEdit()
        email_row.addWidget(self._username_entry, 1)
        card_layout.addLayout(email_row)

        pw_row = QHBoxLayout()
        self._pw_label = QLabel("Password:")
        self._pw_label.setFixedWidth(70)
        sp = self._pw_label.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self._pw_label.setSizePolicy(sp)
        pw_row.addWidget(self._pw_label)
        self._password_entry = QLineEdit()
        self._password_entry.setEchoMode(QLineEdit.Password)
        sp = self._password_entry.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self._password_entry.setSizePolicy(sp)
        pw_row.addWidget(self._password_entry, 1)
        card_layout.addLayout(pw_row)

        self._account_group.buttonClicked[int].connect(
            self._on_account_mode_changed,
        )

        ver_row = QHBoxLayout()
        ver_label = QLabel("Version:")
        ver_label.setFixedWidth(70)
        ver_row.addWidget(ver_label)
        self._version_combo = QComboBox()
        ver_row.addWidget(self._version_combo, 1)
        self._remember_check = QCheckBox("Remember")
        ver_row.addWidget(self._remember_check)
        card_layout.addLayout(ver_row)

        layout.addWidget(card)

        layout.addSpacing(16)

        self._play_btn = QPushButton(f"{_ICON_PLAY}  PLAY")
        self._play_btn.setObjectName("play_button")
        self._play_btn.clicked.connect(self._on_play)
        layout.addWidget(self._play_btn)

        layout.addStretch(1)

    def refresh(self) -> None:
        config = self._app.config

        self._account_group.blockSignals(True)
        if config.premium:
            self._premium_btn.setChecked(True)
        else:
            self._offline_btn.setChecked(True)
        self._account_group.blockSignals(False)

        self._username_label.setText("Email:" if config.premium else "Username:")
        self._set_pw_visible(config.premium)
        self._username_entry.setText(config.email)

        versions = self._app.get_versions()
        if config.last_selected and config.last_selected not in versions:
            versions.insert(0, config.last_selected)

        self._version_combo.clear()
        self._version_combo.addItems(versions)

    def _set_pw_visible(self, visible: bool) -> None:
        self._pw_label.setVisible(visible)
        self._password_entry.setVisible(visible)

    def _on_account_mode_changed(self, button_id: int) -> None:
        is_premium = button_id == 0
        self._username_label.setText("Email:" if is_premium else "Username:")
        self._set_pw_visible(is_premium)

    def _on_play(self) -> None:
        username = self._username_entry.text()
        version = self._version_combo.currentText()
        remember_me = self._remember_check.isChecked()

        if not username:
            warning_box("PyMyMC Error!", "Username cannot be empty!")
            return

        if not version:
            warning_box(
                "PyMyMC Error!",
                "No version selected! Download one from the Versions page.",
            )
            return

        self._app.config.premium = self._premium_btn.isChecked()
        self.window().close()
        self._app.play(
            username=username,
            version=version,
            remember_me=remember_me,
        )
