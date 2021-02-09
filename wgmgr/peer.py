from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import Any

from . import keygen


class Peer:
    def __init__(
        self,
        hostname: str,
        private_key: str | None = None,
        public_key: str | None = None,
    ):
        self.hostname: str = hostname
        self.private_key = (
            keygen.generate_private_key() if private_key is None else private_key
        )
        self.public_key = (
            keygen.generate_public_key(self.private_key)
            if public_key is None
            else public_key
        )
        self.ipv4_address: IPv4Address | None = None
        self.ipv4_auto: bool | None = None
        self.ipv6_address: IPv6Address | None = None
        self.ipv6_auto: bool | None = None
        self.port: int | None = None
        self.port_auto: bool | None = None

    def regenerate_key(self):
        self.private_key = keygen.generate_private_key()
        self.public_key = keygen.generate_public_key(self.private_key)

    def to_config_entry(self) -> dict[str, Any]:
        yml: dict[str, Any] = {
            "hostname": self.hostname,
            "private_key": self.private_key,
            "public_key": self.public_key,
        }

        if self.ipv4_address is not None:
            yml["ipv4"] = str(self.ipv4_address)

        if self.ipv4_auto is not None:
            yml["ipv4_auto"] = self.ipv4_auto

        if self.ipv6_address is not None:
            yml["ipv6"] = str(self.ipv6_address)

        if self.ipv6_auto is not None:
            yml["ipv6_auto"] = self.ipv6_auto

        if self.port is not None:
            yml["port"] = self.port

        if self.port_auto is not None:
            yml["port_auto"] = self.port_auto

        return yml

    @staticmethod
    def from_config_entry(entry: dict[str, Any]) -> Peer:
        peer = Peer(entry["hostname"], entry["private_key"], entry["public_key"])

        peer.ipv4_address = IPv4Address(entry["ipv4"]) if "ipv4" in entry else None
        peer.ipv4_auto = entry.get("ipv4_auto", None)
        peer.ipv6_address = IPv6Address(entry["ipv6"]) if "ipv6" in entry else None
        peer.ipv6_auto = entry.get("ipv6_auto", None)
        peer.port = entry.get("port", None)
        peer.port_auto = entry.get("port_auto", None)

        return peer
