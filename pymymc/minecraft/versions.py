from __future__ import annotations

import glob
import platform
import traceback

from natsort import natsorted

from pymymc.log import log_error
from pymymc.minecraft.ports import VersionProvider

_SYSTEM = platform.system()


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

    # Merge locally installed versions.
    version_folders = glob.glob(minecraft_dir + "versions/*/")
    for version_dir in version_folders:
        sep = "\\" if _SYSTEM == "Windows" else "/"
        version_name = version_dir.split(sep)[-2]
        if version_name not in versions:
            versions.append(version_name)

    if not show_historical:
        versions = [v for v in versions if not v.startswith("b")]

    return natsorted(versions, reverse=True)
