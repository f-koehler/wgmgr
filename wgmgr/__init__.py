from __future__ import annotations

import logging
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import Any, Generic, TypeVar, cast

from wgmgr import keygen

LOGGER = logging.getLogger(__name__)


class DuplicatePeerError(Exception):
    def __init__(self, name: str):
        super().__init__(f"peer already exists: {name}")


class UnknownPeerError(Exception):
    def __init__(self, name: str):
        super().__init__(f"unknown peer: {name}")


class FreeAddressError(Exception):
    def __init__(self, protocol: str):
        super().__init__(f"no free {protocol} address")


Value = TypeVar("Value")


class AutoAssignable(Generic[Value]):
    def __init__(self, value: Value, auto_assigned: bool):
        self.value: Value = value
        self.auto_assigned: bool = auto_assigned

    def serialize(self) -> dict[str, Any]:
        return {"value": self.value, "auto": self.auto_assigned}

    @staticmethod
    def deserialize(data: dict[str, Any]):
        obj = AutoAssignable[Value](
            cast(Value, data["value"]),
            data["auto"],
        )
        return obj


class GlobalConfig:
    def __init__(self):
        self.ipv4_network: IPv4Network | None
        self.ipv6_network: IPv6Network | None
        self.default_port: int
        self.peers: list[PeerConfig]
        self.point_to_point: list[PointToPointConfig]

    def set_default_port(self, port: int):
        if port == self.default_port:
            LOGGER.warn("port already set to %d, nothing to do", port)
            return

        self.default_port = port
        for peer in self.peers:
            if peer.port.auto_assigned:
                LOGGER.info("set port to %d for peer %s", port, peer.name)
                peer.port.value = port

    def add_peer(
        self,
        name: str,
        ipv4: IPv4Address | None = None,
        ipv6: IPv6Address | None = None,
        port: int | None = None,
    ):
        for peer in self.peers:
            if peer.name == name:
                raise DuplicatePeerError(name)

        private_key = keygen.generate_private_key()
        peer = PeerConfig(name, private_key, keygen.generate_public_key(private_key))

        if ipv4:
            peer.ipv4 = AutoAssignable[IPv4Address](ipv4, False)
        else:
            if ipv4 := self.get_next_ipv4():
                LOGGER.info("assign IPv4 address %s to peer %s", str(ipv4), peer)
                peer.ipv4 = AutoAssignable[IPv4Address](ipv4, True)

        if ipv6:
            peer.ipv6 = AutoAssignable[IPv6Address](ipv6, False)
        else:
            if ipv6 := self.get_next_ipv6():
                LOGGER.info("assign IPv6 address %s to peer %s", str(ipv6), peer)
                peer.ipv6 = AutoAssignable[IPv6Address](ipv6, True)

        if port:
            peer.port = AutoAssignable[int](port, False)
        else:
            peer.port = AutoAssignable[int](self.default_port, True)

    def regenerate_all_keys(self):
        for peer in self.peers:
            self.regenerate_keys_for_peer(peer.name)

    def regenerate_keys_for_peer(self, name: str):
        peer = self.get_peer(name)

        old_public_key = peer.public_key

        peer.private_key = keygen.generate_private_key()
        peer.public_key = keygen.generate_public_key(peer.private_key)

        for p2p in self.point_to_point:
            if p2p.host1_public_key == old_public_key:
                p2p.host1_public_key = peer.public_key
                p2p.preshared_key = keygen.generate_psk()
            elif p2p.host2_public_key == old_public_key:
                p2p.host2_public_key = peer.public_key
                p2p.preshared_key = keygen.generate_psk()

    def get_peer(self, name: str) -> PeerConfig:
        for peer in self.peers:
            if peer.name == name:
                return peer
        raise UnknownPeerError(name)

    def get_next_ipv4(self) -> IPv4Address | None:
        if self.ipv4_network is None:
            return None
        raise FreeAddressError("IPv4")

    def get_next_ipv6(self) -> IPv6Address | None:
        if self.ipv6_network is None:
            return None
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
    def deserialize(data: dict[str, Any]) -> GlobalConfig:
        config = GlobalConfig()
        config.ipv4_network = (
            IPv4Network(data["ipv4_network"]) if data["ipv4_network"] else None
        )
        config.ipv6_network = (
            IPv6Network(data["ipv6_network"]) if data["ipv6_network"] else None
        )
        config.default_port = int(data["default_port"])
        config.peers = [PeerConfig.deserialize(entry) for entry in data["peers"]]
        config.point_to_point = [
            PointToPointConfig.deserialize(entry) for entry in data["point_to_point"]
        ]

        return config


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


class PointToPointConfig:
    def __init__(self):
        self.host1_public_key: str
        self.host2_public_key: str
        self.host1_endpoint: str | None
        self.host2_endpoint: str | None
        self.preshared_key: str

    def serialize(self) -> dict[str, Any]:
        return {
            "host1": {
                "public_key": self.host1_public_key,
                "endpoint": self.host1_endpoint if self.host1_endpoint else None,
            },
            "host2": {
                "public_key": self.host2_public_key,
                "endpoint": self.host2_endpoint if self.host2_endpoint else None,
            },
            "preshared_key": self.preshared_key,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> PointToPointConfig:
        config = PointToPointConfig()
        config.host1_public_key = data["host1"]["public_key"]
        config.host1_endpoint = data["host1"]["endpoint"]
        config.host2_public_key = data["host2"]["public_key"]
        config.host2_endpoint = data["host2"]["endpoint"]
        config.preshared_key = data["preshared_key"]
        return config
