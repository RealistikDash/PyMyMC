from __future__ import annotations

import random
from datetime import datetime

from colorama import Fore
from colorama import init

init()

ASCII = r""" _____       __  __       __  __  _____
 |  __ \     |  \/  |     |  \/  |/ ____|
 | |__) |   _| \  / |_   _| \  / | |
 |  ___/ | | | |\/| | | | | |\/| | |
 | |   | |_| | |  | | |_| | |  | | |____
 |_|    \__, |_|  |_|\__, |_|  |_|\_____|
         __/ |        __/ |
        |___/        |___/   by RealistikDash
"""

_COLOURS = (
    Fore.YELLOW,
    Fore.MAGENTA,
    Fore.BLUE,
    Fore.WHITE,
    Fore.CYAN,
    Fore.GREEN,
)


def _format_time(fmt: str = "%H:%M:%S") -> str:
    return datetime.now().strftime(fmt)


def log_coloured(content: str, colour: str) -> None:
    print(colour + content + Fore.RESET)


def log_info(content: str) -> None:
    log_coloured(f"[{_format_time()}] {content}", Fore.BLUE)


def log_warning(content: str) -> None:
    log_coloured(f"[{_format_time()}] {content}", Fore.YELLOW)


def log_error(content: str) -> None:
    log_coloured(f"[{_format_time()}] {content}", Fore.RED)


def print_banner() -> None:
    log_coloured(ASCII, random.choice(_COLOURS))
