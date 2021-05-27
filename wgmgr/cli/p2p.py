from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer

from wgmgr.cli import common

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
    pass


@app.command()
def list(
    config_path: Path = common.OPTION_CONFIG_PATH,
):
    pass
