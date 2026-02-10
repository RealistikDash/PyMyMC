from __future__ import annotations

import shutil
from pathlib import Path

import minecraft_launcher_lib
import requests

from pymymc.minecraft.ports import InstallCallbacks


class MinecraftAdapter:
    def get_release_ids(self) -> list[str]:
        data = requests.get(
            "https://launchermeta.mojang.com/mc/game/version_manifest.json",
        ).json()
        return [ver["id"] for ver in data["versions"] if ver["type"] == "release"]

    def is_vanilla_version(self, version: str) -> bool:
        known_ids = [v["id"] for v in minecraft_launcher_lib.utils.get_version_list()]
        return version in known_ids

    def install(
        self,
        version: str,
        minecraft_dir: Path,
        callbacks: InstallCallbacks,
    ) -> None:
        callback_dict = {
            "setStatus": callbacks.set_status,
            "setProgress": callbacks.set_progress,
            "setMax": callbacks.set_max,
        }
        minecraft_launcher_lib.install.install_minecraft_version(
            version,
            str(minecraft_dir),
            callback=callback_dict,
        )

    def is_installed(self, version: str, minecraft_dir: Path) -> bool:
        return (minecraft_dir / "versions" / version).exists()

    def uninstall(self, version: str, minecraft_dir: Path) -> None:
        version_path = minecraft_dir / "versions" / version
        if version_path.is_dir():
            shutil.rmtree(version_path)

    def get_all_version_ids(self) -> list[str]:
        data = requests.get(
            "https://launchermeta.mojang.com/mc/game/version_manifest.json",
        ).json()
        return [ver["id"] for ver in data["versions"]]

    def get_launch_command(
        self,
        version: str,
        minecraft_dir: Path,
        options: dict,
    ) -> list[str]:
        return minecraft_launcher_lib.command.get_minecraft_command(
            version,
            str(minecraft_dir),
            options,
        )
