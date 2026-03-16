from __future__ import annotations

from abc import ABC

from enum import StrEnum


class Language(StrEnum):
    """Represents all of the supported languages."""

    ENGLISH = "english"


class Text(ABC):
    """Represents a unique string without a specified language, but that can
    later be translated to a specific language."""

    def app_name(self) -> str:
        return "app_name"
