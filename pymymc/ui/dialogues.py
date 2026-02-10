from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

from pymymc.constants import ui as c
from pymymc.log import log_error
from pymymc.log import log_info
from pymymc.log import log_warning

_ICON_INFO = "\u2139"
_ICON_ERROR = "\u2715"
_ICON_WARNING = "\u26A0"

_CARD_STYLE = (
    f"QFrame#dialog_card {{ background: {c.BG_SURFACE};"
    f"border: 1px solid {c.BORDER_SUBTLE};"
    f"border-radius: {c.DIALOGUE_BORDER_RADIUS}px; }}"
    f"QFrame#dialog_card QLabel {{ background: transparent; border: none; }}"
    f"QFrame#dialog_card QPushButton {{ border: none; }}"
)
_ICON_STYLE = f"color: {{accent}}; font-size: {c.DIALOGUE_ICON_FONT_SIZE}px;"
_TITLE_STYLE = (
    f"color: {c.TEXT_PRIMARY};"
    f"font-size: {c.DIALOGUE_TITLE_FONT_SIZE}px; font-weight: bold;"
)
_CONTENT_STYLE = (
    f"color: {c.TEXT_SECONDARY}; font-size: {c.DIALOGUE_CONTENT_FONT_SIZE}px;"
)
_BTN_STYLE = (
    f"QPushButton {{{{ background-color: {{accent}}; color: {c.TEXT_PRIMARY};"
    f"font-weight: bold; border-radius: {c.DIALOGUE_BTN_BORDER_RADIUS}px;"
    f"padding: 6px {c.DIALOGUE_PADDING}px; }}}}"
    f"QPushButton:hover {{{{ background-color: {{accent}}; opacity: 0.9; }}}}"
)


def _show_dialog(
    title: str,
    content: str,
    icon: str,
    accent: str,
) -> None:
    parent = QApplication.activeWindow()
    dlg = QDialog(parent)
    dlg.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
    dlg.setModal(True)
    dlg.setAttribute(Qt.WA_TranslucentBackground)

    # Card frame — the visible rounded container
    card = QFrame(dlg)
    card.setObjectName("dialog_card")
    card.setStyleSheet(_CARD_STYLE)
    card.setFixedWidth(c.DIALOGUE_WIDTH)

    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(c.DIALOGUE_SHADOW_BLUR)
    shadow.setOffset(0, c.DIALOGUE_SHADOW_OFFSET)
    shadow.setColor(Qt.black)
    card.setGraphicsEffect(shadow)

    # Icon
    icon_lbl = QLabel(icon)
    icon_lbl.setStyleSheet(_ICON_STYLE.format(accent=accent))
    icon_lbl.setFixedWidth(c.DIALOGUE_ICON_WIDTH)
    icon_lbl.setAlignment(Qt.AlignTop)

    # Title
    title_lbl = QLabel(title)
    title_lbl.setStyleSheet(_TITLE_STYLE)
    title_lbl.setWordWrap(True)

    # Content
    content_lbl = QLabel(content)
    content_lbl.setStyleSheet(_CONTENT_STYLE)
    content_lbl.setWordWrap(True)

    # OK button
    ok_btn = QPushButton("OK")
    ok_btn.setFixedWidth(c.DIALOGUE_BTN_WIDTH)
    ok_btn.setCursor(Qt.PointingHandCursor)
    ok_btn.setStyleSheet(_BTN_STYLE.format(accent=accent))
    ok_btn.clicked.connect(dlg.accept)

    # Layout inside the card
    text_col = QVBoxLayout()
    text_col.setSpacing(c.DIALOGUE_TEXT_SPACING)
    text_col.addWidget(title_lbl)
    text_col.addWidget(content_lbl)

    top_row = QHBoxLayout()
    top_row.setAlignment(Qt.AlignTop)
    top_row.addWidget(icon_lbl)
    top_row.addLayout(text_col, 1)

    btn_row = QHBoxLayout()
    btn_row.addStretch()
    btn_row.addWidget(ok_btn)

    card_layout = QVBoxLayout(card)
    card_layout.setContentsMargins(
        c.DIALOGUE_PADDING,
        c.DIALOGUE_PADDING,
        c.DIALOGUE_PADDING,
        c.DIALOGUE_PADDING,
    )
    card_layout.setSpacing(c.DIALOGUE_PADDING)
    card_layout.addLayout(top_row)
    card_layout.addLayout(btn_row)

    # Dialog layout just holds the card
    dlg_layout = QVBoxLayout(dlg)
    dlg_layout.setContentsMargins(0, 0, 0, 0)
    dlg_layout.addWidget(card)

    dlg.exec_()


def message_box(title: str, content: str) -> None:
    _show_dialog(title, content, icon=_ICON_INFO, accent=c.ACCENT)
    log_info(content)


def error_box(title: str, content: str) -> None:
    _show_dialog(title, content, icon=_ICON_ERROR, accent=c.DANGER)
    log_error(content)


def warning_box(title: str, content: str) -> None:
    _show_dialog(title, content, icon=_ICON_WARNING, accent=c.WARNING)
    log_warning(content)
