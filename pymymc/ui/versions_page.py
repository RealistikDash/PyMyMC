from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from pymymc.app import InstallResult
from pymymc.ui.dialogues import error_box
from pymymc.ui.dialogues import message_box

if TYPE_CHECKING:
    from pymymc.app import App


class _ProgressSignals(QObject):
    status_changed = pyqtSignal(str)
    progress_changed = pyqtSignal(int)
    max_changed = pyqtSignal(int)
    install_finished = pyqtSignal()


class VersionsPage(QWidget):
    def __init__(self, app: App, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._app = app
        self._signals = _ProgressSignals()
        self._versions: list[str] = []
        self._installed: set[str] = set()
        self._downloading = False
        self._callbacks_wired = False
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Versions")
        title.setObjectName("page_title")
        layout.addWidget(title)

        desc = QLabel("Download and manage Minecraft versions")
        desc.setObjectName("page_desc")
        layout.addWidget(desc)

        filter_row = QHBoxLayout()
        filter_row.setSpacing(8)
        self._search_entry = QLineEdit()
        self._search_entry.setPlaceholderText("Search versions...")
        self._search_entry.textChanged.connect(self._apply_filter)
        filter_row.addWidget(self._search_entry, 1)

        self._releases_only_check = QCheckBox("Releases only")
        self._releases_only_check.setChecked(True)
        self._releases_only_check.toggled.connect(self._on_filter_toggled)
        filter_row.addWidget(self._releases_only_check)
        layout.addLayout(filter_row)

        self._version_list = QListWidget()
        self._version_list.currentItemChanged.connect(self._on_selection_changed)
        layout.addWidget(self._version_list, 1)

        button_row = QHBoxLayout()
        button_row.setSpacing(8)

        self._download_btn = QPushButton("Download")
        self._download_btn.setEnabled(False)
        self._download_btn.clicked.connect(self._on_download)
        button_row.addWidget(self._download_btn)

        self._delete_btn = QPushButton("Delete")
        self._delete_btn.setObjectName("delete_button")
        self._delete_btn.setEnabled(False)
        self._delete_btn.clicked.connect(self._on_delete)
        button_row.addWidget(self._delete_btn)

        button_row.addStretch()
        layout.addLayout(button_row)

        self._progress_bar = QProgressBar()
        self._progress_bar.setValue(0)
        self._progress_bar.setFormat("")
        layout.addWidget(self._progress_bar)

        self._signals.status_changed.connect(self._on_progress_status)
        self._signals.progress_changed.connect(self._on_progress_value)
        self._signals.max_changed.connect(self._on_progress_max)
        self._signals.install_finished.connect(self._on_install_complete)

    def showEvent(self, event: object) -> None:
        super().showEvent(event)
        if not self._callbacks_wired:
            self._wire_callbacks()
        self._load_versions()

    def hideEvent(self, event: object) -> None:
        super().hideEvent(event)
        if self._callbacks_wired and not self._downloading:
            self._unwire_callbacks()

    def _wire_callbacks(self) -> None:
        cb = self._app.install_callbacks
        self._orig_on_status = cb.on_status
        self._orig_on_progress = cb.on_progress
        self._orig_on_max = cb.on_max
        self._orig_on_complete = cb.on_complete

        cb.on_status = self._signals.status_changed.emit
        cb.on_progress = self._signals.progress_changed.emit
        cb.on_max = self._signals.max_changed.emit
        cb.on_complete = self._signals.install_finished.emit
        self._callbacks_wired = True

    def _unwire_callbacks(self) -> None:
        cb = self._app.install_callbacks
        cb.on_status = self._orig_on_status
        cb.on_progress = self._orig_on_progress
        cb.on_max = self._orig_on_max
        cb.on_complete = self._orig_on_complete
        self._callbacks_wired = False

    def _load_versions(self) -> None:
        releases_only = self._releases_only_check.isChecked()
        self._versions = self._app.get_available_versions(releases_only)
        self._installed = set(self._app.get_versions())

        for local in self._installed:
            if local not in self._versions:
                self._versions.append(local)

        self._apply_filter()

    def _apply_filter(self) -> None:
        search = self._search_entry.text().lower()
        self._version_list.clear()

        for version in self._versions:
            if search and search not in version.lower():
                continue
            installed = version in self._installed
            label = f"{version}  [installed]" if installed else version
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, version)
            self._version_list.addItem(item)

        self._download_btn.setEnabled(False)
        self._delete_btn.setEnabled(False)

    def _on_selection_changed(self) -> None:
        if self._downloading:
            return
        item = self._version_list.currentItem()
        if item is None:
            self._download_btn.setEnabled(False)
            self._delete_btn.setEnabled(False)
            return
        version = item.data(Qt.UserRole)
        installed = version in self._installed
        self._download_btn.setEnabled(not installed)
        self._delete_btn.setEnabled(installed)

    def _on_download(self) -> None:
        item = self._version_list.currentItem()
        if item is None:
            return
        version = item.data(Qt.UserRole)
        result = self._app.install(version)

        if result == InstallResult.ALREADY_INSTALLED:
            message_box("PyMyMC Info!", "This version is already installed!")
        elif result == InstallResult.NO_INTERNET:
            error_box(
                "PyMyMC Error!",
                "An internet connection is required for this action!",
            )
        elif result == InstallResult.DOWNLOADING:
            self._downloading = True
            self._download_btn.setEnabled(False)
            self._delete_btn.setEnabled(False)

    def _on_install_complete(self) -> None:
        self._downloading = False
        self._installed = set(self._app.get_versions())
        self._progress_bar.setValue(0)
        self._progress_bar.setFormat("")
        self._apply_filter()

    def _on_delete(self) -> None:
        item = self._version_list.currentItem()
        if item is None:
            return
        version = item.data(Qt.UserRole)
        self._app.uninstall(version)
        self._installed.discard(version)
        self._apply_filter()

    def _on_filter_toggled(self) -> None:
        self._load_versions()

    def _on_progress_status(self, status: str) -> None:
        self._progress_bar.setValue(0)
        self._progress_bar.setFormat(status)

    def _on_progress_value(self, value: int) -> None:
        self._progress_bar.setValue(int(value))

    def _on_progress_max(self, maximum: int) -> None:
        self._progress_bar.setMaximum(int(maximum))
