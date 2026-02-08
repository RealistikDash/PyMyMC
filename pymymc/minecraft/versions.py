from __future__ import annotations

import glob
import platform
import traceback

from natsort import natsorted

from pymymc.log import log_error
from pymymc.minecraft.ports import VersionProvider

_SYSTEM = platform.system()


def _get_local_versions(minecraft_dir: str) -> list[str]:
    sep = "\\" if _SYSTEM == "Windows" else "/"
    return [path.split(sep)[-2] for path in glob.glob(minecraft_dir + "versions/*/")]


def get_installed_versions(minecraft_dir: str) -> list[str]:
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
    minecraft_dir: str,
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
