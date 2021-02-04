from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import Generator, List, Optional

from . import keygen
from .peer import Peer


class Config:
    def __init__(
        self,
        ipv4_subnet: Optional[IPv4Network] = None,
        ipv6_subnet: Optional[IPv6Network] = None,
        default_port: int = 51902,
    ):
        self.peers: List[Peer] = []
        self.network_ipv4 = ipv4_subnet
        self.network_ipv6 = ipv6_subnet
        self.default_port = default_port

    def add_peer(self, hostname: str, port: Optional[int] = None) -> Peer:
        private_key = keygen.generate_private_key()
        peer = Peer(
            hostname,
            private_key,
            keygen.generate_public_key(private_key),
            port=self.default_port,
        )

        if self.network_ipv4:
            peer.ipv4_address = self.get_free_ipv4()

        if self.network_ipv6:
            peer.ipv6_address = self.get_free_ipv6()

        return peer

    def get_addresses_ipv4(self) -> Generator[IPv4Address, None, None]:
        for peer in self.peers:
            if peer.ipv4_address:
                yield peer.ipv4_address

    def get_addresses_ipv6(self) -> Generator[IPv6Address, None, None]:
        for peer in self.peers:
            if peer.ipv6_address:
                yield peer.ipv6_address

    def get_free_ipv4(self) -> IPv4Address:
        if not self.network_ipv4:
            raise ValueError("no IPv4 network specified")

        addresses = set(self.get_addresses_ipv4())
        for address in self.network_ipv4:
            if address not in addresses:
                return address
        raise RuntimeError("all IPv4 addresses already occupied")

    def get_free_ipv6(self) -> IPv6Address:
        if not self.network_ipv6:
            raise ValueError("no IPv6 network specified")

        addresses = set(self.get_addresses_ipv6())
        for address in self.network_ipv6:
            if address not in addresses:
                return address
        raise RuntimeError("all IPv6 addresses already occupied")
