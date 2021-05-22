from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import Any


class AssignablePort:
    def __init__(self, number: int, auto: bool):
        self.number = number
        self.auto = auto

    def set(self, number: int, auto: bool):
        self.number = number
        self.auto = auto

    def set_auto(self, number: int):
        self.set(number, True)

    def set_manual(self, number: int):
        self.set(number, True)

    def serialize(self) -> dict[str, Any]:
        return {"number": self.number, "auto": self.auto}

    @staticmethod
    def deserialize(data: dict[str, Any]) -> AssignablePort:
        return AssignablePort(int(data["number"]), bool(data["auto"]))


class AssignableIPv4:
    def __init__(self, address: IPv4Address, auto: bool):
        self.address = address
        self.auto = auto

    def set(self, address: IPv4Address, auto: bool):
        self.address = address
        self.auto = auto

    def set_auto(self, address: IPv4Address):
        self.set(address, True)

    def set_manual(self, address: IPv4Address):
        self.set(address, False)

    def serialize(self) -> dict[str, Any]:
        return {"address": str(self.address), "auto": self.auto}

    @staticmethod
    def deserialize(data: dict[str, Any]) -> AssignableIPv4:
        return AssignableIPv4(IPv4Address(data["address"]), bool(data["auto"]))


class AssignableIPv6:
    def __init__(self, address: IPv6Address, auto: bool):
        self.address = address
        self.auto = auto

    def set(self, address: IPv6Address, auto: bool):
        self.address = address
        self.auto = auto

    def set_auto(self, address: IPv6Address):
        self.set(address, True)

    def set_manual(self, address: IPv6Address):
        self.set(address, False)

    def serialize(self) -> dict[str, Any]:
        return {"address": str(self.address), "auto": self.auto}

    @staticmethod
    def deserialize(data: dict[str, Any]) -> AssignableIPv6:
        return AssignableIPv6(IPv6Address(data["address"]), bool(data["auto"]))
