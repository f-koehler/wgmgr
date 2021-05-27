import logging
from ipaddress import IPv4Network, IPv6Network
from pathlib import Path
from typing import Optional

from typer import Option, Typer, echo

from wgmgr.cli import common, p2p, peer
from wgmgr.config.main import MainConfig

logging.basicConfig(level=logging.INFO)

app = Typer()
app.add_typer(peer.app, name="peer", help="Manage peers.")
app.add_typer(
    p2p.app, name="p2p", help="Manage point-to-point connections between peers."
)


@app.command()
def new(
    config_path: Path = common.OPTION_CONFIG_PATH,
    ipv4_network: Optional[str] = common.OPTION_IPV4_NETWORK,
    ipv6_network: Optional[str] = common.OPTION_IPV6_NETWORK,
    default_port: Optional[int] = common.OPTION_PORT,
    force: bool = Option(
        False, "-f", "--force", help="Force overwriting of existing config file"
    ),
):
    """
    Create a new empty config file.
    """
    if config_path.exists() and (not force):
        echo(
            f'config file "{config_path}" exists, add -f/--force flag to overwrite',
            err=True,
        )
        exit(1)

    if default_port is None:
        default_port = 51820

    if ipv4_network is None:
        ipv4_network = "10.0.0.0/24"

    if ipv6_network is None:
        ipv6_network = "fd00:641:c767:bc00::/64"

    config = MainConfig(
        default_port, IPv4Network(ipv4_network), IPv6Network(ipv6_network)
    )
    config.save(config_path)


@app.command()
def set(
    config_path: Path = common.OPTION_CONFIG_PATH,
    port: Optional[int] = common.OPTION_PORT,
    ipv4_network: Optional[str] = common.OPTION_IPV4_NETWORK,
    ipv6_network: Optional[str] = common.OPTION_IPV6_NETWORK,
):
    """
    Change global and default settings.

    If a new IPv4/IPv6 subnet is specified, all automatically assigned IPv4/IPv6
    addresses will be regenerated. Manually set IP addresses will be overwritten
    if they are not contained in the new subnet.

    If a new port is specified, all peers that do not have a manually assigned port
    will be set to use the new default.
    """

    config = MainConfig.load(config_path)
    if port is not None:
        config.set_default_port(port)
    if ipv4_network is not None:
        config.set_ipv4_network(IPv4Network(ipv4_network))
    if ipv6_network is not None:
        config.set_ipv6_network(IPv6Network(ipv6_network))
    config.save(config_path)


@app.command()
def migrate(
    config_path: Path = common.OPTION_CONFIG_PATH,
):
    """
    Load config file, migrate it to the newest version and save it.
    """
    config = MainConfig.load(config_path)
    config.save(config_path)


if __name__ == "__main__":
    app()
