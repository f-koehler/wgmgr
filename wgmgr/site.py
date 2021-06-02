from __future__ import annotations

from typing import Any


class Site:
    def __init__(self, name: str):
        self.name = name

    def serialize(self) -> dict[str, Any]:
        return {"name": self.name}

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Site:
        return Site(data["name"])
