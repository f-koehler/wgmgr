from __future__ import annotations

import logging
from ipaddress import IPv4Network, IPv6Network

import wgmgr.config.main.operations.config as ops_config
import wgmgr.config.main.operations.peer as ops_peer
from wgmgr import keygen
from wgmgr.config.main.base import MainConfigBase

LOGGER = logging.getLogger(__name__)


class MainConfig(MainConfigBase):
    add_peer = ops_peer.add_peer
    set_default_port = ops_config.set_default_port
    ipv4_set_network = ops_config.set_ipv4_network
    ipv6_set_network = ops_config.set_ipv6_network

    def __init__(
        self,
        default_port: int,
        ipv4_network: IPv4Network | None = None,
        ipv6_network: IPv6Network | None = None,
    ):
        super().__init__(default_port, ipv4_network, ipv6_network)

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
