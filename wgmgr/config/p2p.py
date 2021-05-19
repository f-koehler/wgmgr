from __future__ import annotations

from typing import Any


class PointToPointConfig:
    def __init__(self):
        self.host1_public_key: str
        self.host2_public_key: str
        self.host1_endpoint: str | None
        self.host2_endpoint: str | None
        self.preshared_key: str

    def serialize(self) -> dict[str, Any]:
        return {
            "host1": {
                "public_key": self.host1_public_key,
                "endpoint": self.host1_endpoint if self.host1_endpoint else None,
            },
            "host2": {
                "public_key": self.host2_public_key,
                "endpoint": self.host2_endpoint if self.host2_endpoint else None,
            },
            "preshared_key": self.preshared_key,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> PointToPointConfig:
        config = PointToPointConfig()
        config.host1_public_key = data["host1"]["public_key"]
        config.host1_endpoint = data["host1"]["endpoint"]
        config.host2_public_key = data["host2"]["public_key"]
        config.host2_endpoint = data["host2"]["endpoint"]
        config.preshared_key = data["preshared_key"]
        return config
