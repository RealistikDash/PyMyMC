from __future__ import annotations

import platform
from tkinter import E
from tkinter import IntVar
from tkinter import Label
from tkinter import StringVar
from tkinter import Toplevel
from tkinter import ttk
from tkinter import W
from typing import TYPE_CHECKING

from pymymc import constants
from pymymc.ui.dialogs import error_box

if TYPE_CHECKING:
    from tkinter import Misc

    from pymymc.app import App

_SYSTEM = platform.system()


class ConfigDialog:
    def __init__(self, parent: Misc, app: App) -> None:
        self._app = app
        self._parent = parent
        self._build()

    def _build(self) -> None:
        self._app.rpc.set_configuring()
        config = self._app.config

        self._window = Toplevel(self._parent)
        self._window.configure(background=constants.ui.BG_COLOUR)
        self._window.title("PyMyMC Config")
        self._window.protocol("WM_DELETE_WINDOW", self._on_close)
        if _SYSTEM == "Windows":
            self._parent.iconbitmap(constants.ui.LOGO_ICON)
        self._window.resizable(False, False)

        Label(
            self._window,
            text="Warning! These options are for advanced users only!",
            bg=constants.ui.BG_COLOUR,
            fg="white",
            font="none 12",
        ).grid(row=0, column=0, sticky=W)
        Label(
            self._window,
            text="Proceed with caution!",
            bg=constants.ui.BG_COLOUR,
            fg="yellow",
            font="none 12 bold",
        ).grid(row=1, column=0, sticky=W)

        Label(
            self._window,
            text="Minecraft Path:",
            bg=constants.ui.BG_COLOUR,
            fg="white",
            font="none 11",
        ).grid(row=2, column=0, sticky=W)

        self._mc_path_var = StringVar(value=config.minecraft_dir)
        ttk.Entry(
            self._window,
            width=40,
            textvariable=self._mc_path_var,
        ).grid(row=3, column=0, sticky=W)

        Label(
            self._window,
            text="JVM Dedicated RAM:",
            bg=constants.ui.BG_COLOUR,
            fg="white",
            font="none 11",
        ).grid(row=4, column=0, sticky=W)

        self._dram_var = StringVar(value=str(config.jvm_ram))
        ttk.Entry(
            self._window,
            width=10,
            textvariable=self._dram_var,
        ).grid(row=5, column=0, sticky=W)

        Label(
            self._window,
            text="GB",
            bg=constants.ui.BG_COLOUR,
            fg="white",
            font="none 9",
        ).grid(row=5, column=0, sticky=E)

        self._forget_me_var = IntVar()
        ttk.Checkbutton(
            self._window,
            text="Forget Me",
            variable=self._forget_me_var,
        ).grid(row=6, column=0, sticky=W)

        self._premium_var = IntVar(value=1 if config.premium else 0)
        ttk.Checkbutton(
            self._window,
            text="Use Premium Minecraft Accounts",
            variable=self._premium_var,
        ).grid(row=7, column=0, sticky=W)

        self._historical_var = IntVar(value=1 if config.show_historical else 0)
        ttk.Checkbutton(
            self._window,
            text="Show non-release versions",
            variable=self._historical_var,
        ).grid(row=8, column=0, sticky=W)

        ttk.Button(
            self._window,
            text="Apply",
            width=constants.ui.BOX_WIDTH,
            command=self._apply,
        ).grid(row=9, column=0, sticky=W)

        ttk.Button(
            self._window,
            text="Cancel",
            width=constants.ui.BOX_WIDTH,
            command=self._window.destroy,
        ).grid(row=9, column=0, sticky=E)

    def _on_close(self) -> None:
        self._window.destroy()
        self._app.rpc.set_main_menu()

    def _apply(self) -> None:
        mc_path = self._mc_path_var.get()
        dram_str = self._dram_var.get()

        try:
            dram_value = int(dram_str)
            if dram_value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            error_box(
                "PyMyMC Error!",
                "The RAM value has to be an integer (full number) over 0.",
            )
            return

        config = self._app.config

        if self._forget_me_var.get() == 1:
            config.email = ""
            config.uuid = ""
            config.access_token = ""

        config.jvm_ram = dram_value

        if _SYSTEM == "Windows":
            if not mc_path.endswith("\\"):
                mc_path += "\\"
        else:
            if not mc_path.endswith("/"):
                mc_path += "/"

        config.minecraft_dir = mc_path
        config.premium = self._premium_var.get() == 1
        config.only_releases = self._historical_var.get() == 0

        self._app.save_config()
        self._window.destroy()
        self._app.notify_config_changed()
