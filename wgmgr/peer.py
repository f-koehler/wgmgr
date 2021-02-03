from typing import List, Optional
from __future__ import annotations
from ipaddress import IPv4Address, IPv6Address

import keygen


class Peer:
    def __init__(self, hostname: str, private_key: str, public_key: str):
        self.hostname: str = hostname
        self.private_key: str = private_key
        self.public_key: str = public_key
        self.ipv4_address: Optional[IPv4Address] = None
        self.ipv6_address: Optional[IPv6Address] = None

    @staticmethod
    def new(hostname: str) -> Peer:
        private_key = keygen.generate_private_key()
        return Peer(hostname, private_key, keygen.generate_public_key(private_key))