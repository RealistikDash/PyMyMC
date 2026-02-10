from __future__ import annotations

import os

# Backgrounds (darkest -> lightest)
BG_DARKEST = "#08080C"
BG_PRIMARY = "#0E0F14"
BG_SURFACE = "#151620"
BG_ELEVATED = "#1C1D2A"

# Borders
BORDER_SUBTLE = "#1E1F2E"
BORDER = "#2A2B3D"

# Text
TEXT_PRIMARY = "#E8EAED"
TEXT_SECONDARY = "#7C7E8C"
TEXT_DISABLED = "#3E3F4D"

# Accent (indigo -> violet gradient)
ACCENT = "#6366F1"
ACCENT_LIGHT = "#818CF8"
ACCENT_GRADIENT_END = "#A855F7"

# Semantic
SUCCESS = "#22C55E"
DANGER = "#EF4444"
DANGER_HOVER = "#DC2626"
WARNING = "#F59E0B"

# Legacy aliases
WARNING_COLOUR = WARNING

# Resources
_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
LOGO_SMALL = os.path.join(_RESOURCES_DIR, "pymymc_logo_small.png")
LOGO_ICON = os.path.join(_RESOURCES_DIR, "pymymc_ico.ico")
