from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer, echo

from wgmgr.cli import common
from wgmgr import MainConfig
from wgmgr.operations.peer import PeerConfigType
from wgmgr.error import DuplicatePeerError, UnknownPeerError, UnknownSiteError

app = Typer()


@app.command()
def add(
    name: str = Argument(..., help="Name of the peer."),
    config_path: Path = common.OPTION_CONFIG_PATH,
    port: Optional[int] = common.OPTION_PORT,
    ipv4_address: Optional[str] = common.OPTION_IPV4_ADDRESS,
    ipv6_address: Optional[str] = common.OPTION_IPV6_ADDRESS,
    site: Optional[str] = None,
):
    """
    Add a new peer.
    """
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
    """
    Remove a new peer.
    """
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
    """
    List peers in the config.
    """
    config = MainConfig.load(config_path)
    for peer in config.peers:
        if verbose:
            echo(peer.serialize())
        else:
            echo(peer.name)


@app.command()
def generate_config(
    name: str = Argument(..., help="Name of the peer."),
    config_type: PeerConfigType = PeerConfigType.wg_quick,
    config_path: Path = common.OPTION_CONFIG_PATH,
):
    """
    Generate config file for a peer.
    """
    config = MainConfig.load(config_path)
    echo(config.generate_peer_config(name, config_type))
