from __future__ import annotations

import traceback
from pathlib import Path

from natsort import natsorted

from pymymc.log import log_error
from pymymc.minecraft.ports import VersionProvider


def _get_local_versions(minecraft_dir: Path) -> list[str]:
    versions_dir = minecraft_dir / "versions"
    if not versions_dir.is_dir():
        return []
    return [p.name for p in versions_dir.iterdir() if p.is_dir()]


def get_installed_versions(minecraft_dir: Path) -> list[str]:
    return natsorted(_get_local_versions(minecraft_dir), reverse=True)


def get_available_versions(
    provider: VersionProvider,
    releases_only: bool,
) -> list[str]:
    try:
        versions = provider.get_release_ids()
    except Exception:
        log_error(
            "Failed fetching releases from web with error:\n" + traceback.format_exc(),
        )
        versions = []

    if not releases_only:
        try:
            all_versions = provider.get_all_version_ids()
            for v in all_versions:
                if v not in versions:
                    versions.append(v)
        except Exception:
            pass

    return natsorted(versions, reverse=True)


def build_version_list(
    provider: VersionProvider,
    minecraft_dir: Path,
    show_historical: bool,
) -> list[str]:
    try:
        versions = provider.get_release_ids()
    except Exception:
        log_error(
            "Failed fetching releases from web with error:\n" + traceback.format_exc(),
        )
        versions = []

    for version_name in _get_local_versions(minecraft_dir):
        if version_name not in versions:
            versions.append(version_name)

    if not show_historical:
        versions = [v for v in versions if not v.startswith("b")]

    return natsorted(versions, reverse=True)
