from __future__ import annotations

from typing import Any

from wgmgr.util import AssignableIPv4, AssignableIPv6, AssignablePort


class PeerConfig:
    def __init__(
        self, name: str, private_key: str, public_key: str, site: str | None = None
    ):
        self.name: str = name
        self.private_key: str = private_key
        self.public_key: str = public_key
        self.ipv4: AssignableIPv4 | None
        self.ipv6: AssignableIPv6 | None
        self.port: AssignablePort
        self.site: str | None

    def serialize(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "private_key": self.private_key,
            "public_key": self.public_key,
            "ipv4": self.ipv4.serialize() if self.ipv4 else None,
            "ipv6": self.ipv6.serialize() if self.ipv6 else None,
            "port": self.port.serialize(),
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> PeerConfig:
        config = PeerConfig(data["name"], data["private_key"], data["public_key"])
        config.ipv4 = AssignableIPv4.deserialize(data["ipv4"]) if data["ipv4"] else None
        config.ipv6 = AssignableIPv6.deserialize(data["ipv6"]) if data["ipv6"] else None
        config.port = AssignablePort.deserialize(data["port"])
        return config
