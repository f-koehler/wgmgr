from __future__ import annotations

from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import Any

from wgmgr.config.p2p import PointToPointConfig
from wgmgr.config.peer import PeerConfig
from wgmgr.error import FreeAddressError, UnknownPeerError


class MainConfigBase:
    def __init__(
        self,
        default_port: int,
        ipv4_network: IPv4Network | None = None,
        ipv6_network: IPv6Network | None = None,
    ):
        self.ipv4_network = ipv4_network
        self.ipv6_network = ipv6_network
        self.default_port = default_port
        self.peers: list[PeerConfig] = []
        self.point_to_point: list[PointToPointConfig] = []

    def get_peer(self, name: str) -> PeerConfig:
        for peer in self.peers:
            if peer.name == name:
                return peer
        raise UnknownPeerError(name)

    def get_used_ipv4_addresses(self) -> list[IPv4Address]:
        result: list[IPv4Address] = []
        for peer in self.peers:
            if peer.ipv4:
                result.append(peer.ipv4.value)
        return result

    def get_used_ipv6_addresses(self) -> list[IPv6Address]:
        result: list[IPv6Address] = []
        for peer in self.peers:
            if peer.ipv6:
                result.append(peer.ipv6.value)
        return result

    def get_next_ipv4(self) -> IPv4Address | None:
        if not self.ipv4_network:
            return None

        used = self.get_used_ipv4_addresses()
        for address in self.ipv4_network.hosts():
            if address in used:
                continue
            return address

        raise FreeAddressError("IPv4")

    def get_next_ipv6(self) -> IPv6Address | None:
        if not self.ipv6_network:
            return None

        used = self.get_used_ipv6_addresses()
        for address in self.ipv6_network.hosts():
            if address in used:
                continue
            return address

        raise FreeAddressError("IPv6")

    def serialize(self) -> dict[str, Any]:
        return {
            "ipv4_network": str(self.ipv4_network) if self.ipv4_network else None,
            "ipv6_network": str(self.ipv6_network) if self.ipv6_network else None,
            "default_port": self.default_port,
            "peers": [peer.serialize() for peer in self.peers],
            "point_to_point": [p2p.serialize() for p2p in self.point_to_point],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> MainConfigBase:
        config = MainConfigBase(
            int(data["default_port"]),
            IPv4Network(data["ipv4_network"]) if data["ipv4_network"] else None,
            IPv6Network(data["ipv6_network"]) if data["ipv6_network"] else None,
        )
        config.peers = [PeerConfig.deserialize(entry) for entry in data["peers"]]
        config.point_to_point = [
            PointToPointConfig.deserialize(entry) for entry in data["point_to_point"]
        ]

        return config
