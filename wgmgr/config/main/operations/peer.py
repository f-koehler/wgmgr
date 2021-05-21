from __future__ import annotations

import logging
from ipaddress import IPv4Address, IPv6Address

from wgmgr import keygen
from wgmgr.config.main.base import MainConfigBase
from wgmgr.config.peer import PeerConfig
from wgmgr.error import DuplicatePeerError
from wgmgr.util import AutoAssignable

LOGGER = logging.getLogger(__name__)


def add_peer(
    self: MainConfigBase,
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
