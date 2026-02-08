from __future__ import annotations

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from pymymc.app import App
from pymymc.ui.main_window import MainWindow

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
qt_app = QApplication(sys.argv)

app = App()
window = MainWindow(app)
window.run()
