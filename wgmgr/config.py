from typing import List, Generator
from ipaddress import IPv4Network, IPv4Address, IPv6Network, IPv6Address

from peer import Peer
import keygen


class Config:
    def __init__(
        self, ipv4_subnet: Optional[str] = None, ipv6_subnet: Optional[str] = None
    ):
        self.peers: List[Peer] = []
        self.network_ipv4: Optional[IPv4Network] = (
            IPv4Network(ipv4_subnet) if ipv4_subnet else None
        )
        self.network_ipv6: Optional[IPv6Network] = (
            IPv6Network(ipv6_subnet) if ipv6_subnet else None
        )

    def add_peer(self, hostname: str) -> Peer:
        private_key = keygen.generate_private_key()
        peer = Peer(hostname, private_key, keygen.generate_public_key(private_key))

        if self.network_ipv4:
            peer.ipv4_address = self.get_free_ipv4()

        if self.network_ipv6:
            peer.ipv4_address = self.get_free_ipv6()

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