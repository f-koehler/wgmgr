from __future__ import annotations

import logging
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import cast

from wgmgr.base import MainConfigBase
from wgmgr.util import AssignableIPv4, AssignableIPv6

LOGGER = logging.getLogger(__name__)


def set_default_port(self: MainConfigBase, port: int):
    if port == self.default_port:
        LOGGER.warn("port already set to %d, nothing to do", port)
        return

    self.default_port = port
    for peer in self.peers:
        if peer.port.auto:
            LOGGER.info("set port to %d for peer %s", port, peer.name)
            peer.port.set_auto(port)


def set_ipv4_network(self: MainConfigBase, network: IPv4Network):
    self.ipv4_network = network
    for peer in self.peers:
        if peer.ipv4:
            if peer.ipv4.address in self.ipv4_network:
                continue
            if not peer.ipv4.auto:
                LOGGER.warn(
                    f"udpating IPv4 address of peer {peer} as it is not "
                    "included in the new network"
                )
            peer.ipv4.set_auto(cast(IPv4Address, self.get_next_ipv4()))
        else:
            peer.ipv4 = AssignableIPv4(cast(IPv4Address, self.get_next_ipv4()), True)


def set_ipv6_network(self: MainConfigBase, network: IPv6Network):
    self.ipv6_network = network
    for peer in self.peers:
        if peer.ipv6:
            if peer.ipv6.address in self.ipv6_network:
                continue
            if not peer.ipv6.auto:
                LOGGER.warn(
                    f"udpating manual IPv6 address of peer {peer} as it is not "
                    "included in the new network"
                )
            peer.ipv6.set_auto(cast(IPv6Address, self.get_next_ipv6()))
        else:
            peer.ipv6 = AssignableIPv6(cast(IPv6Address, self.get_next_ipv6()), True)
