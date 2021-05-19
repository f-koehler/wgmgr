from __future__ import annotations

import logging
import os
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from pathlib import Path
from typing import Any

import yaml

from wgmgr import keygen
from wgmgr.config.p2p import PointToPointConfig
from wgmgr.config.peer import PeerConfig
from wgmgr.error import DuplicatePeerError, FreeAddressError, UnknownPeerError
from wgmgr.util import AutoAssignable

LOGGER = logging.getLogger(__name__)


class MainConfig:
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

    def save(self, path: Path):
        with os.fdopen(
            os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode=0o600), "w"
        ) as fptr:
            yaml.dump(self.serialize(), fptr, yaml.CDumper)

    @staticmethod
    def load(path: Path) -> MainConfig:
        with os.fdopen(os.open(path, os.O_RDONLY, mode=0o600), "r") as fptr:
            return MainConfig.deserialize(yaml.load(fptr, yaml.CLoader))

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
    def deserialize(data: dict[str, Any]) -> MainConfig:
        config = MainConfig(
            int(data["default_port"]),
            IPv4Network(data["ipv4_network"]) if data["ipv4_network"] else None,
            IPv6Network(data["ipv6_network"]) if data["ipv6_network"] else None,
        )
        config.peers = [PeerConfig.deserialize(entry) for entry in data["peers"]]
        config.point_to_point = [
            PointToPointConfig.deserialize(entry) for entry in data["point_to_point"]
        ]

        return config
