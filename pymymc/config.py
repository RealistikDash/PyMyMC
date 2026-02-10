from __future__ import annotations

import json
import os
import platform
from dataclasses import dataclass
from pathlib import Path

if platform.system() == "Windows":
    _DEFAULT_MC_DIR = Path(os.environ["APPDATA"]) / ".minecraft"
else:
    _DEFAULT_MC_DIR = Path.home() / ".minecraft"


@dataclass
class AppConfig:
    minecraft_dir: Path = _DEFAULT_MC_DIR
    email: str = ""
    uuid: str = ""
    access_token: str = ""
    premium: bool = True
    last_selected: str = "1.15.1"
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


class ConfigManager:
    def __init__(self, path: Path = Path("config.json")) -> None:
        self._path = path

    def load(self) -> AppConfig:
        if not self._path.exists():
            config = AppConfig()
            self.save(config)
            return config

        with open(self._path) as f:
            raw = json.load(f)

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
