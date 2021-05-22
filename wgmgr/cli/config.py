from __future__ import annotations

from ipaddress import IPv4Network, IPv6Network
from pathlib import Path

from typer import Option, Typer, echo

from wgmgr.cli import common
from wgmgr.config.main import MainConfig

app = Typer()


@app.command()
def new(
    config_path: Path = common.OPTION_CONFIG_PATH,
    ipv4_network: str | None = common.OPTION_IPV4_NETWORK,
    ipv6_network: str | None = common.OPTION_IPV6_NETWORK,
    default_port: int | None = common.OPTION_PORT,
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
    port: int | None = common.OPTION_PORT,
    ipv4_network: str | None = common.OPTION_IPV4_NETWORK,
    ipv6_network: str | None = common.OPTION_IPV6_NETWORK,
):
    """
    Change default properties of the config and update peers accordingly.

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
