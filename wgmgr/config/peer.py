from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import Any

from wgmgr.util import AutoAssignable


class PeerConfig:
    def __init__(self, name: str, private_key: str, public_key: str):
        self.name: str
        self.private_key: str
        self.public_key: str
        self.ipv4: AutoAssignable[IPv4Address] | None
        self.ipv6: AutoAssignable[IPv6Address] | None
        self.port: AutoAssignable[int]

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
        config.ipv4 = (
            AutoAssignable[IPv4Address].deserialize(data["ipv4"])
            if data["ipv4"]
            else None
        )
        config.ipv6 = (
            AutoAssignable[IPv6Address].deserialize(data["ipv6"])
            if data["ipv6"]
            else None
        )
        config.port = AutoAssignable[int].deserialize(data["port"])
        return config
