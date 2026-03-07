from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from pymymc.app import App
from pymymc.ui.main_window import MainWindow

qt_app = QApplication(sys.argv)

app = App()
window = MainWindow(app)
window.run()
