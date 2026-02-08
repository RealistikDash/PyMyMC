from __future__ import annotations

from pypresence import Presence

from pymymc import constants


class DiscordRPC:
    def __init__(self, enabled: bool, client_id: str) -> None:
        self._client = None
        if enabled:
            self._client = Presence(client_id)
            self._client.connect()

    def set_main_menu(self) -> None:
        if self._client:
            self._client.update(
                state="In the main menu.",
                large_image=constants.rpc.LARGE_IMAGE,
                small_image=constants.rpc.ROOT_IMAGE,
            )

    def set_configuring(self) -> None:
        if self._client:
            self._client.update(
                state="Configuring things...",
                small_image=constants.rpc.CONFIG_IMAGE,
                large_image=constants.rpc.LARGE_IMAGE,
            )

    def set_playing(
        self,
        version: str,
        username: str,
        is_premium: bool,
        is_vanilla: bool,
    ) -> None:
        if not self._client:
            return

        small_icon = (
            constants.rpc.VANILLA_IMAGE if is_vanilla else constants.rpc.MODDED_IMAGE
        )
        premium_state = "" if is_premium else ", non-premuim"
        self._client.update(
            state=f"Playing Minecraft {version}",
            large_image=constants.rpc.LARGE_IMAGE,
            small_image=small_icon,
            details=f"Playing as {username}{premium_state}",
        )
