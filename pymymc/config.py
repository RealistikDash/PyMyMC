from __future__ import annotations

import json
import os
import platform
from dataclasses import dataclass
from pathlib import Path

from pymymc.log import log_warning

if platform.system() == "Windows":
    _DEFAULT_MC_DIR = (
        Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        / ".minecraft"
    )
else:
    _DEFAULT_MC_DIR = Path.home() / ".minecraft"


def _default_config_dir() -> Path:
    system = platform.system()
    if system == "Windows":
        base = Path(
            os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"),
        )
    elif system == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    d = base / "PyMyMC"
    d.mkdir(parents=True, exist_ok=True)
    return d


@dataclass
class AppConfig:
    minecraft_dir: Path = _DEFAULT_MC_DIR
    email: str = ""
    uuid: str = ""
    access_token: str = ""
    premium: bool = True
    last_selected: str = ""
    only_releases: bool = True
    java_path: str = ""
    custom_resolution: bool = False
    resolution_width: int = 854
    resolution_height: int = 480
    jvm_args: str = "-Xmx2G"
    auto_connect_server: str = ""
    auto_connect_port: int = 25565

    @property
    def show_historical(self) -> bool:
        return not self.only_releases


_KEY_MAP = {
    "MinecraftDir": "minecraft_dir",
    "Email": "email",
    "UUID": "uuid",
    "AccessToken": "access_token",
    "Premium": "premium",
    "LastSelected": "last_selected",
    "OnlyReleases": "only_releases",
    "JavaPath": "java_path",
    "CustomResolution": "custom_resolution",
    "ResolutionWidth": "resolution_width",
    "ResolutionHeight": "resolution_height",
    "JVMArgs": "jvm_args",
    "AutoConnectServer": "auto_connect_server",
    "AutoConnectPort": "auto_connect_port",
}
_REVERSE_KEY_MAP = {v: k for k, v in _KEY_MAP.items()}


_DEFAULT_CONFIG_PATH = _default_config_dir() / "config.json"


class ConfigManager:
    def __init__(self, path: Path = _DEFAULT_CONFIG_PATH) -> None:
        self._path = path

    def load(self) -> AppConfig:
        if not self._path.exists():
            config = AppConfig()
            self.save(config)
            return config

        try:
            with open(self._path) as f:
                raw = json.load(f)
        except (json.JSONDecodeError, PermissionError, OSError) as e:
            log_warning(f"Config file corrupted or unreadable ({e}), using defaults.")
            config = AppConfig()
            self.save(config)
            return config

        if not raw:
            config = AppConfig()
            self.save(config)
            return config

        defaults = AppConfig()
        kwargs = {}
        for json_key, field_name in _KEY_MAP.items():
            kwargs[field_name] = raw.get(json_key, getattr(defaults, field_name))

        # Migrate legacy JVMRAM into JVMArgs
        if "JVMRAM" in raw and "JVMArgs" not in raw:
            ram = raw["JVMRAM"]
            kwargs["jvm_args"] = f"-Xmx{ram}G"

        if isinstance(kwargs.get("minecraft_dir"), str):
            kwargs["minecraft_dir"] = Path(kwargs["minecraft_dir"])

        config = AppConfig(**kwargs)
        self.save(config)
        return config

    def save(self, config: AppConfig) -> None:
        raw = {}
        for field_name, json_key in _REVERSE_KEY_MAP.items():
            value = getattr(config, field_name)
            raw[json_key] = str(value) if isinstance(value, Path) else value
        with open(self._path, "w") as f:
            json.dump(raw, f, indent=4)
