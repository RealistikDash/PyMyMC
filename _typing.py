from __future__ import annotations

from typing import Literal
from typing import TypedDict
from typing import Union

VERSION_TYPES = Literal["snapshot", "release", "old_beta"]


class MinecraftRelease(TypedDict):
    """Typing for a Minecraft version manifest JSON resposne."""

    id: str
    type: VERSION_TYPES
    url: str
    time: str
    releaseTime: str
