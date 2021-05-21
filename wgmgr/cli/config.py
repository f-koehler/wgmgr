from __future__ import annotations

from ipaddress import IPv4Network, IPv6Network
from pathlib import Path

from typer import BadParameter, Option, Typer, echo

from wgmgr.config.main import MainConfig

app = Typer()


DEFAULT_CONFIG_PATH = Path("wgmgr.yml")


def validate_port(port: str) -> str:
    number = int(port)
    if (number < 1) or (number > 65535):
        raise BadParameter("port number must be in the range 1…65535")
    return port


def validate_ipv4_network(cidr: str, required_hosts: int = 2) -> str:
    if cidr == "":
        return cidr

    net = IPv4Network(cidr)
    counter = 0
    for _ in net.hosts():
        counter += 1
        if counter >= required_hosts:
            break
    if counter < required_hosts:
        raise BadParameter("IPv4Network should contain at least 2 hosts")
    return cidr


def validate_ipv6_network(cidr: str, required_hosts: int = 2) -> str:
    if cidr == "":
        return cidr

    net = IPv6Network(cidr)
    counter = 0
    for _ in net.hosts():
        counter += 1
        if counter >= required_hosts:
            break
    if counter < required_hosts:
        raise BadParameter("IPv6Network should contain at least 2 hosts")
    return cidr


@app.command()
def new(
    config_path: Path = Option(
        DEFAULT_CONFIG_PATH,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="Path of the config file.",
    ),
    ipv4_network: str = Option(
        "10.0.0.0/24",
        "-4",
        "--ipv4",
        callback=validate_ipv4_network,
        help="IPv4 network in CIDR notation or empty string to disable IPv4.",
    ),
    ipv6_network: str = Option(
        "fd00:641:c767:bc00::/64",
        "-6",
        "--ipv6",
        callback=validate_ipv6_network,
        help="IPv4 network in CIDR notation or empty string to disable IPv6.",
    ),
    default_port: int = Option(
        "51820", "-p", "--port", callback=validate_port, help="Default port for peers."
    ),
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

    config = MainConfig(
        default_port, IPv4Network(ipv4_network), IPv6Network(ipv6_network)
    )
    config.save(config_path)


@app.command()
def set_port(
    config_path: Path = Option(
        DEFAULT_CONFIG_PATH,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="Path of the config file.",
    ),
    port: int = Option("51820", callback=validate_port, help="Default port for peers."),
):
    """
    Set the default port and upate all peers that use the default.
    """
    config = MainConfig.load(config_path)
    config.set_default_port(port)
    config.save(config_path)


@app.command()
def set_ipv4(
    config_path: Path = Option(
        DEFAULT_CONFIG_PATH,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="Path of the config file.",
    ),
    ipv4_network: str = Option(
        "10.0.0.0/24",
        callback=validate_ipv4_network,
        help="IPv4 network in CIDR notation or empty string to disable IPv4.",
    ),
):
    """
    Set the IPv4 subnet to use and update peers accordingly.

    This will regenerate all automatically assigned IPv4 addresses but also manually set
    ones which are not contained in the new subnet.
    """
    config = MainConfig.load(config_path)
    config.set_ipv4_network(IPv4Network(ipv4_network))
    config.save(config_path)


@app.command()
def set_ipv6(
    config_path: Path = Option(
        DEFAULT_CONFIG_PATH,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="Path of the config file.",
    ),
    ipv6_network: str = Option(
        "fd00:641:c767:bc00::/64",
        callback=validate_ipv4_network,
        help="IPv6 network in CIDR notation or empty string to disable IPv4.",
    ),
):
    """
    Set the IPv6 subnet to use and update peers accordingly.

    This will regenerate all automatically assigned IPv6 addresses but also manually set
    ones which are not contained in the new subnet.
    """
    config = MainConfig.load(config_path)
    config.set_ipv6_network(IPv6Network(ipv6_network))
    config.save(config_path)


@app.command()
def migrate(
    config_path: Path = Option(
        DEFAULT_CONFIG_PATH,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="Path of the config file.",
    )
):
    """
    Load config file, migrate it to the newest version and save it.
    """
    config = MainConfig.load(config_path)
    config.save(config_path)
