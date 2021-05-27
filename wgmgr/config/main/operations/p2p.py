from __future__ import annotations

from wgmgr.config.main.base import MainConfigBase
from wgmgr.config.p2p import PointToPointConfig


def add_p2p(
    self: MainConfigBase,
    name1: str,
    name2: str,
    endpoint1: str | None = None,
    endpoint2: str | None = None,
):
    if name1 > name2:
        name1, name2 = name2, name1
        endpoint1, endpoint2 = endpoint2, endpoint1

    if name1 == name2:
        raise ValueError("Cannot add p2p connection between a peer and itself")

    if endpoint1 and (endpoint1 == endpoint2):
        raise ValueError("The peers in a p2p cannot have the same endpoint address")

    for p2p in self.point_to_point:
        if (p2p.peer1_name == name1) and (p2p.peer2_name == name2):
            raise ValueError(
                f"P2P connection between {name1} and {name2} is already present"
            )
        if (p2p.peer1_name == name2) and (p2p.peer2_name == name1):
            raise ValueError(
                f"P2P connection between {name1} and {name2} is already present"
            )

    self.point_to_point.append(PointToPointConfig(name1, name2, endpoint1, endpoint2))
