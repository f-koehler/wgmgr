from __future__ import annotations

import logging
from ipaddress import IPv4Address, IPv6Address

from wgmgr import keygen
from wgmgr.config.main.base import MainConfigBase
from wgmgr.config.peer import PeerConfig
from wgmgr.error import DuplicatePeerError, UnknownPeerError
from wgmgr.util import AssignableIPv4, AssignableIPv6, AssignablePort

LOGGER = logging.getLogger(__name__)


def add_peer(
    self: MainConfigBase,
    name: str,
    ipv4: IPv4Address | None = None,
    ipv6: IPv6Address | None = None,
    port: int | None = None,
):
    try:
        self.get_peer(name)
        raise DuplicatePeerError(name)
    except UnknownPeerError:
        pass

    private_key = keygen.generate_private_key()
    peer = PeerConfig(name, private_key, keygen.generate_public_key(private_key))

    if ipv4:
        peer.ipv4 = AssignableIPv4(ipv4, False)
    else:
        if ipv4 := self.get_next_ipv4():
            LOGGER.info("assign IPv4 address %s to peer %s", str(ipv4), peer.name)
            peer.ipv4 = AssignableIPv4(ipv4, True)

    if ipv6:
        peer.ipv6 = AssignableIPv6(ipv6, False)
    else:
        if ipv6 := self.get_next_ipv6():
            LOGGER.info("assign IPv6 address %s to peer %s", str(ipv6), peer.name)
            peer.ipv6 = AssignableIPv6(ipv6, True)

    if port:
        peer.port = AssignablePort(port, False)
    else:
        peer.port = AssignablePort(self.default_port, True)

    self.peers.append(peer)


def remove_peer(self: MainConfigBase, name: str):
    self.peers.remove(self.get_peer(name))
