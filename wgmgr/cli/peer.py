from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer, echo

from wgmgr.cli import common
from wgmgr.config.main import MainConfig
from wgmgr.error import DuplicatePeerError, UnknownPeerError

app = Typer()


@app.command()
def add(
    name: str = Argument(..., help="Name of the peer."),
    config_path: Path = common.OPTION_CONFIG_PATH,
    port: Optional[int] = common.OPTION_PORT,
    ipv4_address: Optional[str] = common.OPTION_IPV4_ADDRESS,
    ipv6_address: Optional[str] = common.OPTION_IPV6_ADDRESS,
):
    config = MainConfig.load(config_path)
    try:
        config.add_peer(
            name,
            IPv4Address(ipv4_address) if ipv4_address else None,
            IPv6Address(ipv6_address) if ipv6_address else None,
            port,
        )
    except DuplicatePeerError as e:
        echo(str(e), err=True)
    config.save(config_path)


@app.command()
def remove(
    name: str = Argument(..., help="Name of the peer."),
    config_path: Path = common.OPTION_CONFIG_PATH,
):
    config = MainConfig.load(config_path)
    try:
        config.remove_peer(name)
    except UnknownPeerError:
        echo(f"no such peer: {name}", err=True)
    config.save(config_path)


@app.command()
def list(
    config_path: Path = common.OPTION_CONFIG_PATH,
    verbose: bool = Option(False, "-v", "--verbose"),
):
    config = MainConfig.load(config_path)
    for peer in config.peers:
        if verbose:
            echo(peer.serialize())
        else:
            echo(peer.name)
