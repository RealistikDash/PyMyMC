from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
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

        layout.addSpacing(16)

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
        pw_label = QLabel("Password:")
        pw_label.setFixedWidth(70)
        pw_row.addWidget(pw_label)
        self._password_entry = QLineEdit()
        self._password_entry.setEchoMode(QLineEdit.Password)
        pw_row.addWidget(self._password_entry, 1)
        card_layout.addLayout(pw_row)

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

        self._play_btn = QPushButton("\u25b6  PLAY")
        self._play_btn.setObjectName("play_button")
        self._play_btn.clicked.connect(self._on_play)
        layout.addWidget(self._play_btn)

        layout.addStretch(1)

    def refresh(self) -> None:
        config = self._app.config
        self._username_label.setText("Email:" if config.premium else "Username:")
        self._username_entry.setText(config.email)

        versions = self._app.get_versions()
        if config.last_selected and config.last_selected not in versions:
            versions.insert(0, config.last_selected)

        self._version_combo.clear()
        self._version_combo.addItems(versions)

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

        self.window().close()
        self._app.play(
            username=username,
            version=version,
            remember_me=remember_me,
        )
