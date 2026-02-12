"""Helper utilities for Minecraft version handling."""

from __future__ import annotations

import re
from typing import Pattern

# Compiled regex patterns for performance
RELEASE_PATTERN: Pattern = re.compile(r'^(\d+)\.(\d+)(?:\.(\d+))?$')
RC_PATTERN: Pattern = re.compile(r'^(\d+)\.(\d+)(?:\.(\d+))?-rc(\d+)$')
PRE_PATTERN: Pattern = re.compile(r'^(\d+)\.(\d+)(?:\.(\d+))?-pre(\d+)$')
MODERN_SNAPSHOT_PATTERN: Pattern = re.compile(r'^(\d+)\.(\d+)-snapshot-(\d+)$')
WEEK_SNAPSHOT_PATTERN: Pattern = re.compile(r'^(\d{2})w(\d{2})([a-z])$')
BETA_PATTERN: Pattern = re.compile(r'^b(\d+)\.(\d+)(?:\.(\d+)|_(\d+))?([a-z])?$')
ALPHA_PATTERN: Pattern = re.compile(r'^a(\d+)\.(\d+)(?:\.(\d+)|_(\d+))?([a-z])?$')


def _parse_version(version: str) -> tuple:
    """
    Parse a Minecraft version string into a sortable tuple.

    Returns a tuple of (tier, major, minor, patch, suffix_num, normalized_string)
    that sorts naturally in ascending order (oldest to newest).

    Tier system (higher tier = higher priority when reversed, i.e., newer):
    - Tier 8: Modern snapshots (26.1-snapshot-7)
    - Tier 7: Release versions (1.21.10, 1.20)
    - Tier 6: Release candidates (1.21.11-rc3)
    - Tier 5: Pre-releases (1.21.11-pre5)
    - Tier 4: Week snapshots (25w46a)
    - Tier 3: Special versions (24w14potato, 3D Shareware v1.34)
    - Tier 2: Beta versions (b1.7.3, b1.5_01)
    - Tier 1: Alpha versions (a1.2.6, a1.0.17_04)
    - Tier 0: Unknown/malformed versions
    """
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

    # Pre-releases: 1.X.X-preN
    match = PRE_PATTERN.match(version)
    if match:
        major, minor, patch, pre_num = match.groups()
        return (5, int(major), int(minor), int(patch or 0), int(pre_num), "")

    # Week snapshots: YYwXXa
    match = WEEK_SNAPSHOT_PATTERN.match(version)
    if match:
        year, week, letter = match.groups()
        letter_offset = ord(letter) - ord('a')
        return (4, int(year), int(week), letter_offset, 0, "")

    # Special versions (contains non-standard characters, but starts with digits)
    if version[0].isdigit() and any(c.isalpha() and c not in 'abpresw-.' for c in version):
        # Extract leading digits for rough sorting
        digits = ""
        for c in version:
            if c.isdigit():
                digits += c
            else:
                break
        major = int(digits) if digits else 0
        return (3, major, 0, 0, 0, version)

    # Beta versions: b1.X.X or b1.X_XX
    match = BETA_PATTERN.match(version)
    if match:
        major, minor, patch1, patch2, letter = match.groups()
        patch = int(patch1 or patch2 or 0)
        letter_offset = ord(letter) - ord('a') if letter else 0
        return (2, int(major), int(minor), patch, letter_offset, "")

    # Alpha versions: a1.X.X or a1.X_XX
    match = ALPHA_PATTERN.match(version)
    if match:
        major, minor, patch1, patch2, letter = match.groups()
        patch = int(patch1 or patch2 or 0)
        letter_offset = ord(letter) - ord('a') if letter else 0
        return (1, int(major), int(minor), patch, letter_offset, "")

    # Unknown/malformed versions
    return (0, 0, 0, 0, 0, version)


def sort_minecraft_versions(versions: list[str], reverse: bool = False) -> list[str]:
    """
    Sort Minecraft version strings according to Minecraft versioning semantics.

    This function understands Minecraft's versioning system and properly prioritizes:
    - Modern releases over snapshots
    - Snapshots over legacy versions
    - Beta versions over alpha versions
    - Proper numerical ordering within each version type

    Args:
        versions: List of version strings to sort
        reverse: If True, sort newest versions first (default: False)

    Returns:
        Sorted list of version strings
    """
    if not versions:
        return []

    sorted_versions = sorted(versions, key=_parse_version)

    if reverse:
        sorted_versions.reverse()

    return sorted_versions
