from __future__ import annotations

from PyQt5.QtWidgets import QMessageBox

from pymymc.log import log_error
from pymymc.log import log_info
from pymymc.log import log_warning


def message_box(title: str, content: str) -> None:
    QMessageBox.information(None, title, content)
    log_info(content)


def error_box(title: str, content: str) -> None:
    QMessageBox.critical(None, title, content)
    log_error(content)


def warning_box(title: str, content: str) -> None:
    QMessageBox.warning(None, title, content)
    log_warning(content)
