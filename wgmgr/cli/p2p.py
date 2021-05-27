from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer, echo

from wgmgr.cli import common
from wgmgr.config.main import MainConfig

app = Typer()


@app.command()
def add(
    peer1: str = Argument(..., help="Name of one peer."),
    peer2: str = Argument(..., help="Name of the other peer."),
    endpoint1: Optional[str] = Option(
        None, help="Endpoint address for peer2 to reach peer1."
    ),
    endpoint2: Optional[str] = Option(
        None, help="Endpoint address for peer1 to reach peer2."
    ),
    config_path: Path = common.OPTION_CONFIG_PATH,
):
    """
    Add a new point-to-point connection.
    """
    config = MainConfig.load(config_path)
    config.add_p2p(peer1, peer2, endpoint1, endpoint2)
    config.save(config_path)


@app.command()
def list(
    config_path: Path = common.OPTION_CONFIG_PATH,
    verbose: bool = Option(False, "-v", "--verbose"),
):
    """
    List point-to-point connections
    """
    config = MainConfig.load(config_path)
    for p2p in config.point_to_point:
        if verbose:
            echo(p2p.serialize())
        else:
            echo(f"{p2p.peer1_name} ↔ {p2p.peer2_name}")
