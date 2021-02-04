from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import List, Optional


class Peer:
    def __init__(self, hostname: str, private_key: str, public_key: str, port: int):
        self.hostname: str = hostname
        self.private_key: str = private_key
        self.public_key: str = public_key
        self.ipv4_address: IPv4Address | None = None
        self.ipv6_address: IPv6Address | None = None
        self.port: int = port
