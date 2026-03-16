"""Helper utilities for Minecraft version handling."""

from __future__ import annotations

import re
from re import Pattern

# Compiled regex patterns for performance
RELEASE_PATTERN: Pattern = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?$")
RC_PATTERN: Pattern = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?-rc(\d+)$")
PRE_PATTERN: Pattern = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?-pre(\d+)$")
MODERN_SNAPSHOT_PATTERN: Pattern = re.compile(r"^(\d+)\.(\d+)-snapshot-(\d+)$")
WEEK_SNAPSHOT_PATTERN: Pattern = re.compile(r"^(\d{2})w(\d{2})([a-z])$")
BETA_PATTERN: Pattern = re.compile(r"^b(\d+)\.(\d+)(?:\.(\d+)|_(\d+))?([a-z])?$")
ALPHA_PATTERN: Pattern = re.compile(r"^a(\d+)\.(\d+)(?:\.(\d+)|_(\d+))?([a-z])?$")


def _parse_version(version: str) -> tuple:
    if not version or not isinstance(version, str):
        return (0, 0, 0, 0, 0, str(version))

    # Modern snapshots: X.X-snapshot-N
    match = MODERN_SNAPSHOT_PATTERN.match(version)
    if match:
        major, minor, snapshot_num = match.groups()
        return (8, int(major), int(minor), int(snapshot_num), 0, "")

    # Release versions: 1.X.X or 1.X
    match = RELEASE_PATTERN.match(version)
    if match:
        major, minor, patch = match.groups()
        return (7, int(major), int(minor), int(patch or 0), 0, "")

    # Release candidates: 1.X.X-rcN
    match = RC_PATTERN.match(version)
    if match:
        major, minor, patch, rc_num = match.groups()
        return (6, int(major), int(minor), int(patch or 0), int(rc_num), "")

    match = PRE_PATTERN.match(version)
    if match:
        major, minor, patch, pre_num = match.groups()
        return (5, int(major), int(minor), int(patch or 0), int(pre_num), "")

    match = WEEK_SNAPSHOT_PATTERN.match(version)
    if match:
        year, week, letter = match.groups()
        letter_offset = ord(letter) - ord("a")
        return (4, int(year), int(week), letter_offset, 0, "")

    if version[0].isdigit() and any(
        c.isalpha() and c not in "abpresw-." for c in version
    ):
        # Extract leading digits for rough sorting
        digits = ""
        for c in version:
            if c.isdigit():
                digits += c
            else:
                break
        major = int(digits) if digits else 0
        return (3, major, 0, 0, 0, version)

    match = BETA_PATTERN.match(version)
    if match:
        major, minor, patch1, patch2, letter = match.groups()
        patch = int(patch1 or patch2 or 0)
        letter_offset = ord(letter) - ord("a") if letter else 0
        return (2, int(major), int(minor), patch, letter_offset, "")

    match = ALPHA_PATTERN.match(version)
    if match:
        major, minor, patch1, patch2, letter = match.groups()
        patch = int(patch1 or patch2 or 0)
        letter_offset = ord(letter) - ord("a") if letter else 0
        return (1, int(major), int(minor), patch, letter_offset, "")

    return (0, 0, 0, 0, 0, version)


def sort_minecraft_versions(versions: list[str], reverse: bool = False) -> list[str]:
    if not versions:
        return []

    sorted_versions = sorted(versions, key=_parse_version)

    if reverse:
        sorted_versions.reverse()

    return sorted_versions
