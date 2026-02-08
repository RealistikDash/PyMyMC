from __future__ import annotations

from typing import Callable

from threading import Thread
from tkinter import messagebox

from pymymc.log import log_error
from pymymc.log import log_info
from pymymc.log import log_warning


def _make_log_thread(func: Callable, title: str, content: str) -> None:
    Thread(target=func, args=(title, content)).start()


def message_box(title: str, content: str) -> None:
    _make_log_thread(messagebox.showinfo, title, content)
    log_info(content)


def error_box(title: str, content: str) -> None:
    _make_log_thread(messagebox.showerror, title, content)
    log_error(content)


def warning_box(title: str, content: str) -> None:
    _make_log_thread(messagebox.showwarning, title, content)
    log_warning(content)
