from __future__ import annotations

from ipaddress import IPv4Network, IPv6Network
from pathlib import Path

from typer import BadParameter, Option, Typer, echo

from wgmgr.config.main import MainConfig

app = Typer()


DEFAULT_CONFIG_PATH = Path("/") / "etc" / "wgmgr.conf"


def validate_port(port: str) -> str:
    number = int(port)
    if (number < 1) or (number > 65535):
        raise BadParameter("port number must be in the range 1…65535")
    return port


def validate_ipv4_network(cidr: str) -> str:
    if cidr == "":
        return cidr

    net = IPv4Network(cidr)
    counter = 0
    for _ in net.hosts():
        counter += 1
        if counter >= 2:
            break
    if counter < 2:
        raise BadParameter("IPv4Network should contain at least 2 hosts")
    return cidr


def validate_ipv6_network(cidr: str) -> str:
    if cidr == "":
        return cidr

    net = IPv6Network(cidr)
    counter = 0
    for _ in net.hosts():
        counter += 1
        if counter >= 2:
            break
    if counter < 2:
        raise BadParameter("IPv6Network should contain at least 2 hosts")
    return cidr


@app.command()
def new(
    config_path: Path = Option(
        DEFAULT_CONFIG_PATH,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="path of the config file",
    ),
    ipv4_network: str = Option(
        "10.0.0.0/24",
        "-4",
        "--ipv4",
        callback=validate_ipv4_network,
        help="IPv4 network in CIDR notation or empty string to disable IPv4",
    ),
    ipv6_network: str = Option(
        "fd00:641:c767:bc00::/64",
        "-6",
        "--ipv6",
        callback=validate_ipv6_network,
        help="IPv4 network in CIDR notation or empty string to disable IPv6",
    ),
    default_port: int = Option(
        "51820", "-p", "--port", callback=validate_port, help="default port for peers"
    ),
    force: bool = Option(
        False, "-f", "--force", help="whether to overwrite an existing config file"
    ),
):
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
