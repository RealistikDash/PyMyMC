from __future__ import annotations

import hashlib
import subprocess
from enum import auto
from enum import Enum
from threading import Thread
from typing import Callable

from pymymc import constants
from pymymc.adapters.mclib import MCLibAdapter
from pymymc.adapters.network import check_internet
from pymymc.config import AppConfig
from pymymc.config import ConfigManager
from pymymc.log import log_info
from pymymc.log import print_banner
from pymymc.minecraft.versions import build_version_list
from pymymc.services.discord import DiscordRPC

APP_VERSION = "0.2.0"


class InstallResult(Enum):
    ALREADY_INSTALLED = auto()
    NO_INTERNET = auto()
    DOWNLOADING = auto()


class ProgressCallbacks:
    def __init__(self) -> None:
        self.on_status: Callable[[str], None] = lambda s: print(s)
        self.on_progress: Callable[[int], None] = lambda v: None
        self.on_max: Callable[[int], None] = lambda m: None

    def set_status(self, status: str) -> None:
        self.on_status(status)

    def set_progress(self, value: int) -> None:
        self.on_progress(value)

    def set_max(self, maximum: int) -> None:
        self.on_max(maximum)


class App:
    def __init__(self) -> None:
        print_banner()
        log_info("Checking internet status...")

        self._config_manager = ConfigManager()
        self.config = self._config_manager.load()
        self.has_internet = check_internet()

        self._minecraft = MCLibAdapter()
        self.rpc = DiscordRPC(constants.rpc.ENABLED, constants.rpc.CLIENT_ID)

        self.install_callbacks = ProgressCallbacks()
        self._ui_refresh: Callable[[], None] = lambda: None

    @property
    def version(self) -> str:
        return APP_VERSION

    def set_ui_refresh(self, callback: Callable[[], None]) -> None:
        self._ui_refresh = callback

    def get_versions(self) -> list[str]:
        return build_version_list(
            self._minecraft,
            self.config.minecraft_dir,
            self.config.show_historical,
        )

    def save_config(self) -> None:
        self._config_manager.save(self.config)

    def notify_config_changed(self) -> None:
        self._ui_refresh()

    def install(self, version: str) -> InstallResult:
        if self._minecraft.is_installed(version, self.config.minecraft_dir):
            return InstallResult.ALREADY_INSTALLED

        if not self.has_internet:
            return InstallResult.NO_INTERNET

        Thread(
            target=self._minecraft.install,
            args=(version, self.config.minecraft_dir, self.install_callbacks),
        ).start()
        return InstallResult.DOWNLOADING

    def play(
        self,
        *,
        username: str,
        version: str,
        remember_me: bool,
    ) -> None:
        config = self.config

        if config.premium:
            username, _ = username.split("@")

        options = {
            "username": username,
            "uuid": str(hashlib.md5(str.encode(username)).digest()),
            "token": "",
            "launcherName": "PyMyMC",
            "gameDirectory": config.minecraft_dir,
            "jvmArguments": config.jvm_args.split(),
        }

        if config.java_path:
            options["executablePath"] = config.java_path

        if config.custom_resolution:
            options["customResolution"] = True
            options["resolutionWidth"] = str(config.resolution_width)
            options["resolutionHeight"] = str(config.resolution_height)

        if config.auto_connect_server:
            options["server"] = config.auto_connect_server
            options["port"] = str(config.auto_connect_port)

        if remember_me:
            config.email = username

        config.last_selected = version
        self.save_config()

        command = self._minecraft.get_launch_command(
            version,
            config.minecraft_dir,
            options,
        )

        is_vanilla = self._minecraft.is_vanilla_version(version)
        self.rpc.set_playing(version, username, config.premium, is_vanilla)

        subprocess.call(command)
