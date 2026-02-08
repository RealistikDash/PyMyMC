from __future__ import annotations

import json
import os
import pathlib
import platform
from dataclasses import dataclass

_SYSTEM = platform.system()

if _SYSTEM == "Windows":
    _DEFAULT_MC_DIR = os.getenv("APPDATA") + "\\.minecraft\\"
else:
    _DEFAULT_MC_DIR = str(pathlib.Path.home()) + "/.minecraft/"


@dataclass
class AppConfig:
    minecraft_dir: str = _DEFAULT_MC_DIR
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
    def __init__(self, path: str = "config.json") -> None:
        self._path = path

    def load(self) -> AppConfig:
        if not os.path.exists(self._path):
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

        config = AppConfig(**kwargs)
        self.save(config)
        return config

    def save(self, config: AppConfig) -> None:
        raw = {
            json_key: getattr(config, field_name)
            for field_name, json_key in _REVERSE_KEY_MAP.items()
        }
        with open(self._path, "w") as f:
            json.dump(raw, f, indent=4)
