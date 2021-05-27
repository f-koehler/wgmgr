from __future__ import annotations

from typing import Any

from wgmgr import keygen


class PointToPointConfig:
    def __init__(
        self,
        name1: str,
        name2: str,
        endpoint1: str | None = None,
        endpoint2: str | None = None,
    ):
        self.peer1_name = name1
        self.peer2_name = name2
        self.peer1_endpoint = endpoint1
        self.peer2_endpoint = endpoint2
        self.preshared_key = keygen.generate_psk()

    def serialize(self) -> dict[str, Any]:
        return {
            "peer1": {
                "name": self.peer1_name,
                "endpoint": self.peer1_endpoint if self.peer1_endpoint else None,
            },
            "peer2": {
                "name": self.peer2_name,
                "endpoint": self.peer2_endpoint if self.peer2_endpoint else None,
            },
            "preshared_key": self.preshared_key,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> PointToPointConfig:
        config = PointToPointConfig(
            data["peer1"]["name"],
            data["peer2"]["name"],
            data["peer1"]["endpoint"],
            data["peer2"]["endpoint"],
        )
        config.preshared_key = data["preshared_key"]
        return config
