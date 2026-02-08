from __future__ import annotations

import platform
from tkinter import E
from tkinter import IntVar
from tkinter import Label
from tkinter import PhotoImage
from tkinter import StringVar
from tkinter import ttk
from tkinter import W
from typing import TYPE_CHECKING

from ttkthemes import ThemedTk

from pymymc import constants
from pymymc.app import InstallResult
from pymymc.log import log_info
from pymymc.ui.config_dialog import ConfigDialog
from pymymc.ui.dialogs import error_box
from pymymc.ui.dialogs import message_box
from pymymc.ui.dialogs import warning_box

if TYPE_CHECKING:
    from pymymc.app import App

_SYSTEM = platform.system()


class MainWindow:
    def __init__(self, app: App) -> None:
        self._app = app

        app.set_ui_refresh(self._refresh_versions)
        app.install_callbacks.on_status = self._on_progress_status
        app.install_callbacks.on_progress = self._on_progress_value
        app.install_callbacks.on_max = self._on_progress_max

        self._build()

    def _build(self) -> None:
        log_info("Loading themes...")
        self._root = ThemedTk(theme=constants.ui.THEME)

        log_info("Configuring the UI...")
        s = ttk.Style()
        s.configure(
            "TButton",
            background=constants.ui.FG_COLOUR,
            fieldbackground=constants.ui.FG_COLOUR,
        )
        s.configure(
            "TCheckbutton",
            background=constants.ui.BG_COLOUR,
            foreground="white",
        )
        s.configure(
            "TEntry",
            fieldbackground=constants.ui.FG_COLOUR,
            background=constants.ui.FG_COLOUR,
        )

        self._root.configure(background=constants.ui.BG_COLOUR)
        self._root.title("PyMyMC")
        self._root.resizable(False, False)
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)
        # Linux and Mac systems don't support .ico files as icons.
        if _SYSTEM == "Windows":
            self._root.iconbitmap(constants.ui.LOGO_ICON)

        self._logo_image = PhotoImage(file=constants.ui.LOGO_SMALL)
        logo_label = Label(self._root, image=self._logo_image)
        logo_label["bg"] = logo_label.master["bg"]
        logo_label.grid(row=0, column=0)

        Label(
            self._root,
            text=f"PyMyMC {self._app.version}",
            bg=constants.ui.BG_COLOUR,
            fg="white",
            font="Arial 15 bold",
        ).grid(row=2, column=0, sticky=W)
        Label(
            self._root,
            text="Made by RealistikDash",
            bg=constants.ui.BG_COLOUR,
            fg="white",
            font="none 13",
        ).grid(row=3, column=0, sticky=W)

        self._username_label = Label(
            self._root,
            text="Email:",
            bg=constants.ui.BG_COLOUR,
            fg="white",
            font="none 12",
        )
        self._username_label.grid(row=5, column=0, sticky=W)

        self._username_var = StringVar(value=self._app.config.email)
        self._username_entry = ttk.Entry(
            self._root,
            width=constants.ui.ENTRY_LEN,
            textvariable=self._username_var,
        )
        self._username_entry.grid(row=6, column=0, sticky=W)

        Label(
            self._root,
            text="Password:",
            bg=constants.ui.BG_COLOUR,
            fg="white",
            font="none 12",
        ).grid(row=7, column=0, sticky=W)

        self._password_entry = ttk.Entry(
            self._root,
            width=constants.ui.ENTRY_LEN,
            show="*",
        )
        self._password_entry.grid(row=8, column=0, sticky=W)

        Label(
            self._root,
            text="Version:",
            bg=constants.ui.BG_COLOUR,
            fg="white",
            font="none 12",
        ).grid(row=9, column=0, sticky=W)

        self._version_var = StringVar(self._root)
        self._version_menu = ttk.OptionMenu(self._root, self._version_var, *[])
        self._version_menu.configure(width=constants.ui.LIST_LEN)
        self._version_menu.grid(row=10, column=0, sticky=W)

        self._remember_me_var = IntVar()
        ttk.Checkbutton(
            self._root,
            text="Remember me",
            variable=self._remember_me_var,
        ).grid(row=10, column=0, sticky=E)

        ttk.Button(
            self._root,
            text="Play!",
            width=constants.ui.BOX_WIDTH,
            command=self._on_play,
        ).grid(row=11, column=0, sticky=W)
        ttk.Button(
            self._root,
            text="Config",
            width=constants.ui.BOX_WIDTH,
            command=self._on_config,
        ).grid(row=11, column=0)
        ttk.Button(
            self._root,
            text="Download!",
            width=constants.ui.BOX_WIDTH,
            command=self._on_install,
        ).grid(row=11, column=0, sticky=E)

        self._progress_bar = ttk.Progressbar(
            self._root,
            length=constants.ui.BAR_LEN,
        )
        self._progress_bar.grid(row=12, column=0)

        self._refresh_versions()
        log_info("Done!")

    def _refresh_versions(self) -> None:
        config = self._app.config
        self._username_label["text"] = "Email:" if config.premium else "Username:"

        versions = self._app.get_versions()
        versions.insert(0, config.last_selected)

        self._version_var = StringVar(self._root)
        self._version_menu.destroy()
        self._version_menu = ttk.OptionMenu(
            self._root,
            self._version_var,
            *versions,
        )
        self._version_menu.configure(width=constants.ui.LIST_LEN)
        self._version_menu.grid(row=10, column=0, sticky=W)

    def _on_play(self) -> None:
        username = self._username_entry.get()
        version = self._version_var.get()
        remember_me = self._remember_me_var.get() == 1

        if not username:
            warning_box("PyMyMC Error!", "Username cannot be empty!")
            return

        self._root.destroy()
        self._app.play(
            username=username,
            version=version,
            remember_me=remember_me,
        )

    def _on_install(self) -> None:
        version = self._version_var.get()
        result = self._app.install(version)

        if result == InstallResult.ALREADY_INSTALLED:
            message_box(
                "PyMyMC Info!",
                "This version is already installed! Press play to play it!",
            )
        elif result == InstallResult.NO_INTERNET:
            error_box(
                "PyMyMC Error!",
                "An internet connection is required for this action!",
            )
        elif result == InstallResult.DOWNLOADING:
            message_box(
                "PyMyMC Info!",
                "Downloading started! If you pressed play to download,"
                " the program will freeze.",
            )

    def _on_config(self) -> None:
        ConfigDialog(self._root, self._app)

    def _on_close(self) -> None:
        self._root.destroy()
        exit()

    def _on_progress_status(self, status: str) -> None:
        self._progress_bar["value"] = 0
        print(status)

    def _on_progress_value(self, value: int) -> None:
        self._progress_bar["value"] = int(value)

    def _on_progress_max(self, maximum: int) -> None:
        self._progress_bar["maximum"] = int(maximum)

    def run(self) -> None:
        self._root.mainloop()
