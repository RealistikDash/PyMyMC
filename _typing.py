from typing import (
    TypedDict,
    Union,
    Literal,
)

VERSION_TYPES = Literal[
    "snapshot",
    "release",
    "old_beta"
]

class MinecraftRelease(TypedDict):
    """Typing for a Minecraft version manifest JSON resposne."""

    id: str
    type: VERSION_TYPES
    url: str
    time: str
    releaseTime: str
