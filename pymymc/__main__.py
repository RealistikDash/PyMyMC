from __future__ import annotations

from pymymc.app import App
from pymymc.ui.main_window import MainWindow

app = App()
window = MainWindow(app)
window.run()
