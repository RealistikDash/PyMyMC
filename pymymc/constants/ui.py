from __future__ import annotations

import os

BG_COLOUR = "#2F3136"
FG_COLOUR = "#2c3e50"
ACCENT_COLOUR = "#7289DA"
TEXT_COLOUR = "#FFFFFF"
TEXT_MUTED = "#B9BBBE"
INPUT_BG = "#40444B"
INPUT_BORDER = "#202225"
BUTTON_HOVER = "#677BC4"
WARNING_COLOUR = "#FAA61A"

_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
LOGO_SMALL = os.path.join(_RESOURCES_DIR, "pymymc_logo_small.png")
LOGO_ICON = os.path.join(_RESOURCES_DIR, "pymymc_ico.ico")
