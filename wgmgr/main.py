from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer

from .backends import Backends

application = Typer()


@application.command()
def new_config(
    path: Path = Argument(
        ..., help="path of the new config file", envvar="WGMGR_CONFIG_FILE"
    ),
    backend: Backends = Argument(
        ...,
        help="configuration backend to use",
        envvar="WGMGR_CONFIG_BACKEND",
        case_sensitive=False,
    ),
):
    """Create a new, empty config."""
    pass


@application.command()
def add_peer(
    config: Path = Argument(
        ..., help="path of the config file", envvar="WGMGR_CONFIG_FILE"
    ),
    interactive: bool = Option(
        False,
        "-i",
        "--interactive",
        help="whether to configure the peer interactively",
    ),
    backend: Backends = Argument(
        ...,
        help="configuration backend to use",
        envvar="WGMGR_CONFIG_BACKEND",
        case_sensitive=False,
    ),
):
    """Add a new peer."""
    pass


@application.command()
def list_peers(
    config: Path = Argument(
        ..., help="path of the config file", envvar="WGMGR_CONFIG_FILE"
    ),
    backend: Backends = Argument(
        ...,
        help="configuration backend to use",
        envvar="WGMGR_CONFIG_BACKEND",
        case_sensitive=False,
    ),
):
    """List peers."""
    pass


def run():
    application()


if __name__ == "__main__":
    run()
