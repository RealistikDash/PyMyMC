from __future__ import annotations

from typing import Protocol


class InstallCallbacks(Protocol):
    def set_status(self, status: str) -> None:
        ...

    def set_progress(self, value: int) -> None:
        ...

    def set_max(self, maximum: int) -> None:
        ...


class VersionProvider(Protocol):
    def get_release_ids(self) -> list[str]:
        ...

    def is_vanilla_version(self, version: str) -> bool:
        ...


class Installer(Protocol):
    def install(
        self,
        version: str,
        minecraft_dir: str,
        callbacks: InstallCallbacks,
    ) -> None:
        ...

    def is_installed(self, version: str, minecraft_dir: str) -> bool:
        ...


class Launcher(Protocol):
    def get_launch_command(
        self,
        version: str,
        minecraft_dir: str,
        options: dict,
    ) -> list[str]:
        ...
